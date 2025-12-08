# benchmarking/store_metrics.py
import json
import os
from datetime import datetime

from benchmarking.mongo_client import get_metrics_collection

METRICS_DIR = "benchmarking_results"
os.makedirs(METRICS_DIR, exist_ok=True)


def store_metrics(job_id, metrics):
    """
    Store metrics in:
    1. Local JSON file
    2. MongoDB
    """

    # Always store timestamp
    metrics_with_ts = {
        "job_id": job_id,
        "timestamp": datetime.utcnow().isoformat(),
        **metrics,
    }

    # -------------------------
    # 1. Save to JSON file
    # -------------------------
    out = os.path.join(METRICS_DIR, f"{job_id}_metrics.json")
    with open(out, "w") as f:
        json.dump(metrics_with_ts, f, indent=2)

    # -------------------------
    # 2. Save to MongoDB
    # -------------------------
    try:
        col = get_metrics_collection()
        col.insert_one(metrics_with_ts)
        print(f"[MongoDB] Metrics stored for job {job_id}")

    except Exception as e:
        print(f"[MongoDB] Failed to store metrics: {e}")
