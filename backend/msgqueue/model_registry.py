# msgqueue/model_registry.py
import os
import torch
from .worker_models import SmallCNN

MODEL_DIR = "models"

_registry = {}

def load_model_dynamic(model_path, device):
    ext = os.path.splitext(model_path)[1].lower()

    # Expand easily in future
    if ext in [".pth", ".pt"]:
        model = SmallCNN(num_classes=10)  # or dynamic per config
        ck = torch.load(model_path, map_location=device)

        if isinstance(ck, dict) and "student_state" in ck:
            ck = ck["student_state"]

        try:
            model.load_state_dict(ck)
        except:
            ck = {k.replace("module.", ""): v for k,v in ck.items()}
            model.load_state_dict(ck)

        model.to(device)
        model.eval()
        return model

    raise ValueError(f"Unsupported model type: {ext}")


def get_model(model_name, device):
    """ lazy-load model once """
    if model_name not in _registry:
        path = os.path.join(MODEL_DIR, model_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model {model_name} not found in {MODEL_DIR}")
        _registry[model_name] = load_model_dynamic(path, device)

    return _registry[model_name]


def list_models():
    return [f for f in os.listdir(MODEL_DIR) if not f.startswith(".")]

