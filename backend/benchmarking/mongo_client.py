# benchmarking/mongo_client.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read from environment variables
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB", "finyear")

if not MONGO_URI:
    raise RuntimeError("MONGODB_URI not found in environment (.env)")

_client = None


def get_mongo_client():
    global _client
    if _client is None:
        print(f"[MongoDB] Connecting to: {MONGO_URI}")
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=20000)
    return _client


def get_metrics_collection():
    client = get_mongo_client()
    db = client[DB_NAME]
    return db["inference_metrics"]
