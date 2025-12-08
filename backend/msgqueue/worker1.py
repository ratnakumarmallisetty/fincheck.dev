# msgqueue/worker1.py
import json
import os
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from msgqueue.connection import get_connection
from msgqueue.model_registry import get_model
from benchmarking.system_metrics import get_system_metrics
from benchmarking.health_checks import check_message_queue, check_model_registry
from benchmarking.store_metrics import store_metrics

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

CIFAR_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR_STD = (0.2023, 0.1994, 0.2010)

preprocess = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(mean=CIFAR_MEAN, std=CIFAR_STD),
])

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEFAULT_MODEL = "model_best.pth"


def run_inference(filepath, model):
    usage_before = get_system_metrics()

    img = Image.open(filepath).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        logits = model(tensor)
        probs = F.softmax(logits, dim=1)[0].cpu().tolist()
        pred = int(torch.argmax(logits).item())

    usage_after = get_system_metrics()

    return {
        "class": pred,
        "probabilities": probs,
        "usage": {
            "before": usage_before,
            "after": usage_after,
        }
    }


def build_metrics_dict(job_id, extra: dict | None = None):
    data = {
        "job_id": job_id,
        "system_usage": get_system_metrics(),
        "registry": check_model_registry(),
        "message_queue": check_message_queue(),
    }
    if extra:
        data.update(extra)
    return data


def _normalize_filepath(raw_path: str) -> str:
    """
    Handle both:
    - old jobs with relative path "uploads/xyz.png"
    - new jobs with absolute path "/Users/.../uploads/xyz.png"
    """
    if os.path.isabs(raw_path):
        return raw_path

    # If it's relative (e.g. 'uploads/xyz.png'), force it under backend/uploads
    return os.path.abspath(os.path.join(BASE_DIR, raw_path))


def callback(ch, method, properties, body):
    data = json.loads(body)
    job_id = data.get("job_id")
    raw_path = data.get("filepath")

    print(f"[Worker] Received job: {job_id}")
    print(f"[Worker] Raw filepath from message: {raw_path}")

    filepath = _normalize_filepath(raw_path)
    print(f"[Worker] Normalized filepath: {filepath}")

    # If file does not exist, DON'T crash the worker → just log, store metrics, ack, and move on
    if not os.path.exists(filepath):
        print(f"[Worker] File not found, skipping job {job_id}: {filepath}")

        metrics = build_metrics_dict(job_id, extra={
            "error": "file_not_found",
            "filepath": filepath,
        })
        store_metrics(job_id, metrics)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        model = get_model(DEFAULT_MODEL, DEVICE)
        result = run_inference(filepath, model)

        metrics = build_metrics_dict(job_id)
        store_metrics(job_id, metrics)

        print(f"[Worker] Job {job_id} DONE → Class: {result['class']}")

    except Exception as e:
        # Catch any unexpected error so the worker thread never dies
        print(f"[Worker] Error while processing job {job_id}: {e}")

        metrics = build_metrics_dict(job_id, extra={
            "error": str(e),
            "filepath": filepath,
        })
        store_metrics(job_id, metrics)

    finally:
        # Always ack so bad jobs don't get re-delivered forever
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    """This function is called by main.py to start the worker in a background thread."""
    print("[Worker] Starting worker...")
    print(f"[Worker] BASE_DIR = {BASE_DIR}")
    print(f"[Worker] UPLOAD_DIR = {UPLOAD_DIR}")

    conn = get_connection()
    ch = conn.channel()
    ch.queue_declare(queue="model_queue", durable=True)

    print("[Worker] Waiting for jobs...")

    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue="model_queue", on_message_callback=callback)

    ch.start_consuming()


if __name__ == "__main__":
    start_worker()
