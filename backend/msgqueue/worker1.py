import json
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from msgqueue.connection import get_connection


class SmallCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1,1)),
        )
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x


CHECKPOINT_PATH = "models/model_best.pth"
BENCHMARK_DIR = "benchmarking_results"
os.makedirs(BENCHMARK_DIR, exist_ok=True)

CIFAR_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR_STD = (0.2023, 0.1994, 0.2010)

preprocess = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(mean=CIFAR_MEAN, std=CIFAR_STD),
])


def load_model(path, device):
    model = SmallCNN(num_classes=10)
    ck = torch.load(path, map_location=device)

    if isinstance(ck, dict) and "student_state" in ck:
        ck = ck["student_state"]

    try:
        model.load_state_dict(ck)
    except:
        ck = {k.replace("module.", ""): v for k, v in ck.items()}
        model.load_state_dict(ck)

    model.to(device)
    model.eval()
    return model


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("[Worker] Using device:", DEVICE)

model = load_model(CHECKPOINT_PATH, DEVICE)
print("[Worker] Loaded model successfully")


def run_inference(filepath):
    img = Image.open(filepath).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        logits = model(tensor)
        probs = F.softmax(logits, dim=1)[0].cpu().tolist()
        pred = int(torch.argmax(logits).item())

    return {"class": pred, "probabilities": probs}


def save_result(job_id, data):
    out_path = os.path.join(BENCHMARK_DIR, f"{job_id}.json")
    with open(out_path, "w") as f:
        json.dump(data, f)


def callback(ch, method, properties, body):
    data = json.loads(body)
    job_id = data["job_id"]
    filepath = data["filepath"]

    print(f"[Worker] Received job: {job_id}")

    result = run_inference(filepath)
    save_result(job_id, result)

    print(f"[Worker] Job {job_id} DONE → Class: {result['class']}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    conn = get_connection()
    ch = conn.channel()

    ch.queue_declare(queue="model_queue", durable=True)
    print("[Worker] Waiting for jobs...")

    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(
        queue="model_queue",
        on_message_callback=callback,
        auto_ack=False
    )

    ch.start_consuming()


if __name__ == "__main__":
    main()
