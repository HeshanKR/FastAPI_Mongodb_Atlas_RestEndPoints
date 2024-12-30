from pymongo import MongoClient
from dotenv import load_dotenv
import os
import boto3 

# Load environment variables from the .env file
load_dotenv()

# Get MongoDB credentials from environment variables
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")

# Construct the connection URI
MONGO_URI = (
    f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}"
    f"@modellacluster.u5r6h.mongodb.net/{MONGO_DB}?retryWrites=true&w=majority&ssl=true"
)

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database and collection
db = client[MONGO_DB]

# Define collections
todo_collection = db["todo_collection"]  # Collection for storing todo items
uploads_collection = db["uploads_collection"]  # Collection for storing uploaded file metadata


# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)