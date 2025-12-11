# backend/msgqueue/worker1.py
import json
import os
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms
from backend.msgqueue.connection import get_connection
from backend.msgqueue.model_registry import get_model

from backend.benchmarking.metrics_manager import collect_all_metrics
from backend.benchmarking.store_metrics import store_metrics
from backend.benchmarking.prediction_quality import get_prediction_quality



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    img = Image.open(filepath).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        logits = model(tensor)
        probabilities = F.softmax(logits, dim=1)[0].cpu().tolist()
        prediction = int(torch.argmax(logits).item())

    return prediction, probabilities, tensor


def _normalize_filepath(raw_path: str) -> str:
    if os.path.isabs(raw_path):
        return raw_path
    return os.path.abspath(os.path.join(BASE_DIR, raw_path))


def callback(ch, method, properties, body):
    data = json.loads(body)
    job_id = data.get("job_id")
    raw_path = data.get("filepath")

    print(f"[Worker] Received job: {job_id}")

    filepath = _normalize_filepath(raw_path)
    print(f"[Worker] Normalized filepath: {filepath}")

    if not os.path.exists(filepath):
        print(f"[Worker] File missing for job {job_id}")

        metrics = collect_all_metrics(job_id)
        metrics["error"] = "file_not_found"
        metrics["filepath"] = filepath

        store_metrics(job_id, metrics)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        model = get_model(DEFAULT_MODEL, DEVICE)
        prediction, probabilities, tensor = run_inference(filepath, model)

        metrics = collect_all_metrics(
            job_id=job_id,
            model=model,
            tensor=tensor,
            probabilities=probabilities
        )

        metrics["prediction_quality"] = get_prediction_quality(probabilities)

        store_metrics(job_id, metrics)

        print(f"[Worker] Job {job_id} DONE → Class: {prediction}")

    except Exception as e:
        print(f"[Worker] Error in job {job_id}: {e}")

        metrics = collect_all_metrics(job_id)
        metrics["error"] = str(e)
        metrics["filepath"] = filepath

        store_metrics(job_id, metrics)

    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    print("[Worker] Starting worker...")

    conn = get_connection()
    channel = conn.channel()
    channel.queue_declare(queue="model_queue", durable=True)

    print("[Worker] Waiting for jobs...")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="model_queue", on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    start_worker()
