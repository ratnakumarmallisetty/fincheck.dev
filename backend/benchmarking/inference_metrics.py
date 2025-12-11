import time
import torch

def get_inference_metrics(model, tensor):
    """
    Computes:
    - Cold inference time
    - Warm inference time
    - 10-run avg latency
    """

    # Cold inference
    start = time.time()
    with torch.no_grad():
        _ = model(tensor)
    cold_time = time.time() - start

    # Warm inference
    start = time.time()
    with torch.no_grad():
        _ = model(tensor)
    warm_time = time.time() - start

    # 10-run average
    times = []
    for _ in range(10):
        start = time.time()
        with torch.no_grad():
            _ = model(tensor)
        times.append(time.time() - start)

    avg_latency = sum(times) / len(times)

    return {
        "cold_inference_time": cold_time,
        "warm_inference_time": warm_time,
        "avg_10run_latency": avg_latency,
    }
