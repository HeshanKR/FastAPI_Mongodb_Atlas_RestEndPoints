from fastapi import APIRouter, File, UploadFile, HTTPException
from datetime import datetime , timezone
import os
from config.database import s3_client, db
from models.uploads import FileMetadata
import magic


router = APIRouter()

# File size limit and allowed types
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
ALLOWED_FILE_TYPES = ["application/pdf", "image/png", "image/jpeg", "video/mp4"]

@router.post("/")
async def upload_file(user_id: str, file: UploadFile = File(...)):
    # Read file content and validate size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 25 MB limit")

    # Validate file type using python-magic
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file_content)
    if file_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Reset file read pointer
    file.file.seek(0)

    # Upload file to S3
    file_key = f"uploads/{datetime.now(tz=timezone.utc).strftime('%Y%m%d%H%M%S')}_{file.filename}"
    try:
        s3_client.upload_fileobj(
            file.file,
            os.getenv("AWS_BUCKET_NAME"),
            file_key
        )
        file_url = f"https://{os.getenv('AWS_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_key}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    # Save metadata in MongoDB using the FileMetadata schema
    metadata = FileMetadata(
        user_id=user_id,
        filename=file.filename,
        file_url=file_url,
        file_type=file_type,
        file_size=len(file_content),
        uploaded_at=datetime.now(tz=timezone.utc),
        visibility="public",
        bucket_name=os.getenv("AWS_BUCKET_NAME"),
        storage_key=file_key,
        tags=[],  # You can allow users to add tags if required
        description=""  # You can allow users to add a description if needed
    )

    try:
        db["uploads"].insert_one(metadata.model_dump())  # Convert Pydantic model to dict for MongoDB
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save metadata: {str(e)}")

    return {"message": "File uploaded successfully", "metadata": metadata.model_dump()}

@router.get("/{filename}")
async def get_file(filename: str):
    file_metadata = db["uploads"].find_one({"filename": filename})
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    # Generate a presigned URL for secure access
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": file_metadata["bucket_name"], "Key": file_metadata["storage_key"]},
            ExpiresIn=3600  # URL expires in 1 hour
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate URL: {str(e)}")

    return {"download_url": presigned_url}
