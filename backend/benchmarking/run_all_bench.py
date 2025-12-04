# run_all.py
"""
Run all benchmark modules and store results as a single JSON document in MongoDB.
this is the main file to connect from the frontend when a file gets loaded as this will run all the functions
and once all are compiled they will be properly stored into a json which will be sent to mongodb throught the 
metricsstoremongodb.py
"""

import uuid
import json
from datetime import datetime

from model_loader import load_model
from latency_test import run_latency
from avg_latency import run_avg_latency
from warm_cold_test import run_warm_cold
from entropy_confidence import run_entropy
from cpu_gpu_monitor import run_cpu_gpu_monitor
from memory_uasge import run_memory_usage
from flops_calc_pth import calculate_model_flops

# your mongodb store class
from metrics_store_mongo import MetricsStoreMongoDB


def run_all(model_path):
    model = load_model(model_path)

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:4]

    output = {
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat(),
        "model_name": model.__class__.__name__,
        "flops": calculate_model_flops(model),
        "latency": run_latency(model),
        "avg_latency": run_avg_latency(model),
        "warm_cold": run_warm_cold(model),
        "entropy": run_entropy(model),
        "cpu_gpu": run_cpu_gpu_monitor(),
        "memory": run_memory_usage()
    }

    # also save the file locally (optional)
    with open(f"run_{run_id}.json", "w") as f:
        json.dump(output, f, indent=2)

    return output


def save_to_db(data):
    """
    Save the JSON output to MongoDB using MetricsStoreMongoDB class.
    """
    store = MetricsStoreMongoDB(
        connection_string="YOUR_MONGO_CONNECTION_STRING",
        db_name="benchmarking_db",
        collection_name="model_runs"
    )

    inserted_id = store.insert_record(data)
    print(f"✔ Saved to MongoDB with _id: {inserted_id}")


if __name__ == "__main__":
    model_path = r"backend\models\model_best.pth"

    result = run_all(model_path)
    save_to_db(result)
