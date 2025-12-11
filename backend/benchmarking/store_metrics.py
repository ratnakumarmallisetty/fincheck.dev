# backend/benchmarking/store_metrics.py
import json
import os
from datetime import datetime
from backend.benchmarking.mongo_client import get_metrics_collection

METRICS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(METRICS_DIR, exist_ok=True)

def store_metrics(job_id, metrics):
    """
    Store metrics in:
    1. Local JSON file
    2. MongoDB
    """

    metrics_with_ts = {
        "job_id": job_id,
        "timestamp": datetime.utcnow().isoformat(),
        **metrics,
    }

    # Save JSON
    out_path = os.path.join(METRICS_DIR, f"{job_id}_metrics.json")
    with open(out_path, "w") as f:
        json.dump(metrics_with_ts, f, indent=2)

    # Save to MongoDB
    try:
        col = get_metrics_collection()
        col.insert_one(metrics_with_ts)
        print(f"[MongoDB] Metrics stored for {job_id}")
    except Exception as e:
        print(f"[MongoDB] FAILED to store metrics: {e}")
