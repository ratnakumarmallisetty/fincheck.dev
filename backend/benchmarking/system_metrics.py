# benchmarking/system_metrics.py
import psutil
import subprocess
import shutil


def get_gpu_metrics():
    """
    Returns GPU usage if NVIDIA GPU is available.
    Otherwise returns gpu_available = False.
    """
    if shutil.which("nvidia-smi") is None:
        return {"gpu_available": False}

    try:
        output = subprocess.check_output([
            "nvidia-smi",
            "--query-gpu=utilization.gpu,memory.used,memory.total",
            "--format=csv,noheader,nounits"
        ]).decode().strip()

        util, used, total = map(int, output.split(", "))

        return {
            "gpu_available": True,
            "utilization_percent": util,
            "memory_used_mb": used,
            "memory_total_mb": total,
        }

    except Exception:
        return {"gpu_available": False}


def get_system_metrics():
    """
    Mukesh metrics:
      - CPU usage
      - RAM usage
      - GPU usage (if available)
    """
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_percent": psutil.virtual_memory().percent,
        "gpu": get_gpu_metrics(),
    }
