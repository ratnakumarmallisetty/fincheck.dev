# backend/msgqueue/model_registry.py

import os
import torch
from backend.msgqueue.worker_models import SmallCNN


# --------------------------------------------
# Resolve absolute MODEL_DIR correctly
# backend/
#   models/
# --------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

print(f"[ModelRegistry] MODEL_DIR = {MODEL_DIR}")

_registry = {}


# ---------------------------------------------------------
# Load a model dynamically based on file extension
# ---------------------------------------------------------
def load_model_dynamic(model_path, device):
    ext = os.path.splitext(model_path)[1].lower()

    if ext in [".pth", ".pt"]:
        print(f"[ModelRegistry] Loading model file: {model_path}")

        model = SmallCNN(num_classes=10)

        ck = torch.load(model_path, map_location=device)

        # Handle checkpoint formats
        if isinstance(ck, dict) and "student_state" in ck:
            ck = ck["student_state"]

        try:
            model.load_state_dict(ck)
        except Exception:
            # Sometimes state_dict keys are prefixed with "module."
            ck = {k.replace("module.", ""): v for k, v in ck.items()}
            model.load_state_dict(ck)

        model.to(device)
        model.eval()
        return model

    raise ValueError(f"Unsupported model type: {ext}")


# ---------------------------------------------------------
# Lazy-load models and reuse them
# ---------------------------------------------------------
def get_model(model_name, device):
    """
    Loads model only once, reuses for all jobs.
    Supports multiple different .pth files.
    """
    if model_name not in _registry:

        model_path = os.path.join(MODEL_DIR, model_name)
        print(f"[ModelRegistry] Expected model path: {model_path}")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model {model_name} not found in {MODEL_DIR}"
            )

        _registry[model_name] = load_model_dynamic(model_path, device)

        print(f"[ModelRegistry] Model '{model_name}' loaded and cached.")

    return _registry[model_name]


# ---------------------------------------------------------
# List available models from backend/models/
# ---------------------------------------------------------
def list_models():
    try:
        return [
            f for f in os.listdir(MODEL_DIR)
            if f.lower().endswith((".pth", ".pt")) and not f.startswith(".")
        ]
    except FileNotFoundError:
        return []
