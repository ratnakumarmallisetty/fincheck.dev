import psutil
import subprocess

def get_gpu_usage():
    """Returns GPU utilization % and memory MB using nvidia-smi."""
    try:
        gpu_util = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"]
        )
        gpu_util = int(gpu_util.decode().strip())

        gpu_mem = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"]
        )
        gpu_mem = int(gpu_mem.decode().strip())
    except:
        gpu_util = None
        gpu_mem = None

    return gpu_util, gpu_mem


def get_usage():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent

    gpu_util, gpu_mem = get_gpu_usage()

    return {
        "cpu_percent": cpu,
        "ram_percent": ram,
        "gpu_percent": gpu_util,
        "gpu_memory_mb": gpu_mem,
    }
