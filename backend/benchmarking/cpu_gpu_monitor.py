import psutil
import torch

def get_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_percent = psutil.virtual_memory().percent

    if torch.cuda.is_available():
        gpu_percent = torch.cuda.utilization()
        gpu_mem = torch.cuda.memory_allocated() / (1024 * 1024)
    else:
        gpu_percent = None
        gpu_mem = None

    return {
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "gpu_percent": gpu_percent,
        "gpu_memory_mb": gpu_mem
    }

if __name__ == "__main__":
    print(get_usage())
