import torch
import torch.nn as nn

def load_model(model_path="backend/models/model_best.pth", device=None):
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    checkpoint = torch.load(model_path, map_location=device)

    # Auto-reconstruct student model
    model = checkpoint["model"] if "model" in checkpoint else None
    if model is None:
        raise ValueError("model_best.pth does not contain a 'model' key.")

    model = model.to(device)
    model.eval()

    return model, device
