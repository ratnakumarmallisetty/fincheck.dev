import torch
import time
from model_loader import load_model

def warm_cold_runs(runs=5):
    model, device = load_model()
    dummy_input = torch.randn(1, 1, 28, 28).to(device)

    times = []
    for _ in range(runs):
        start = time.time()
        with torch.no_grad():
            model(dummy_input)
        times.append((time.time() - start) * 1000)

    return {
        "runs": runs,
        "times_ms": times
    }

if __name__ == "__main__":
    print(warm_cold_runs())
