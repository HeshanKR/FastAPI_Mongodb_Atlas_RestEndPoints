from pymongo import MongoClient
from dotenv import load_dotenv
import os

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
collection_name = db["todo_collection"]
