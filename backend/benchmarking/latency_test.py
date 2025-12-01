import time
import torch
from model_loader import load_model

def measure_latency():
    model, device = load_model()
    dummy_input = torch.randn(1, 1, 28, 28).to(device)

    # Cold inference
    start = time.time()
    with torch.no_grad():
        model(dummy_input)
    cold_time = (time.time() - start) * 1000  # ms

    # Warm inference
    start = time.time()
    with torch.no_grad():
        model(dummy_input)
    warm_time = (time.time() - start) * 1000  # ms

    return {
        "cold_inference_ms": cold_time,
        "warm_inference_ms": warm_time
    }

if __name__ == "__main__":
    print(measure_latency())
