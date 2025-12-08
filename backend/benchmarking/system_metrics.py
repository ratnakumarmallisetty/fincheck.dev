import psutil
import subprocess
import json
import shutil
from ..benchmarking.calc_flops import calculate_flops
from ..benchmarking.model_size import get_model_size
from ..benchmarking.get_memory_footprint import get_memory_footprint

def get_gpu_metrics():
    if shutil.which("nvidia-smi") is None:
        return {"gpu_available": False}

    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"]
        ).decode().strip()

        util, mem_used, mem_total = map(int, result.split(", "))

        return {
            "gpu_available": True,
            "utilization": util,
            "memory_used_mb": mem_used,
            "memory_total_mb": mem_total,
        }
    except Exception:
        return {"gpu_available": False}


def get_system_metrics():
    flops_metrics = calculate_flops()
    model_size = get_model_size()
    memory_foot = get_memory_footprint()
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_percent": psutil.virtual_memory().percent,
        "gpu": get_gpu_metrics(),
        "no_of_flops": flops_metrics["flops"],
        "parameters": flops_metrics["params"],
        "model_size":model_size["model_size_mb"],
        "memory_footprint_mb": memory_foot["memory_mb"],
    }



