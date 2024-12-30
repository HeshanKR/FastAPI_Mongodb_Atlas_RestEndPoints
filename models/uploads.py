from pydantic import BaseModel
from datetime import datetime
from typing import List

class FileMetadata(BaseModel):
    user_id: str
    filename: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    visibility: str = "public"
    bucket_name: str
    storage_key: str
    tags: List[str] = []
    description: str = ""
