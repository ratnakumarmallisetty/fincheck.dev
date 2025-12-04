from pymongo import MongoClient
import os

class MetricsStoreMongodb:
    def __init__(self, uri=os.getenv("MONGO_URI"), db_name="benchmarkDB", collection_name="benchmark_runs"):
        self.uri = uri or os.getenv("MONGO_URI")
        self.client = MongoClient(self.uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_run_metrics(self, metrics_dict):
        return str(self.collection.insert_one(metrics_dict).inserted_id)

    def get_all_runs(self):
        return list(self.collection.find({}, {"_id": 0}))

    def get_run_by_id(self, run_id):
        return self.collection.find_one({"run_id": run_id}, {"_id": 0})

    def find(self, query):
        return list(self.collection.find(query, {"_id": 0}))
