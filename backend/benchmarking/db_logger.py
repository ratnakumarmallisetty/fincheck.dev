import json
import datetime

def log_to_db(result_dict, file_path="benchmark_results.json"):
    result_dict["timestamp"] = str(datetime.datetime.now())

    with open(file_path, "a") as f:
        f.write(json.dumps(result_dict) + "\n")

    return True
