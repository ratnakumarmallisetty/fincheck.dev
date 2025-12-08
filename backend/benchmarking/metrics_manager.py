from benchmarking.system_metrics import get_system_metrics


def collect_all_metrics(job_id, model=None, tensor=None, probabilities=None):
    metrics = {
        "job_id": job_id,
        "system_metrics": get_system_metrics(),  
    }

    return metrics
