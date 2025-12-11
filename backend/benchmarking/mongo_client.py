from pymongo import MongoClient
import os

def get_metrics_collection():
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB", "fincheck")

    print(f"[MongoDB] Connecting to: {uri}")

    client = MongoClient(uri)
    db = client[db_name]
    return db["metrics"]
