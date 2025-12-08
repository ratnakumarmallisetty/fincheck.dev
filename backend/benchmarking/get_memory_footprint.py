import torch
import psutil
import os
from ..msgqueue.worker_models import SmallCNN

def get_memory_footprint(model_path=None, input_shape=(1, 3, 224, 224), use_gpu=False, num_classes=10) -> dict:
    if model_path is None:
        backend_root = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(backend_root, "models", "model_best.pth")

    checkpoint = torch.load(model_path, map_location="cpu")
    if "student_state" in checkpoint:
        state_dict = checkpoint["student_state"]
    elif "model_state" in checkpoint:
        state_dict = checkpoint["model_state"]
    else:
        raise KeyError("No valid model weights found in the checkpoint.")

    model = SmallCNN(num_classes=num_classes)
    model.load_state_dict(state_dict)
    model.eval()

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)

    device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
    model.to(device)

    dummy_input = torch.randn(input_shape, device=device)

    if use_gpu:
        torch.cuda.reset_peak_memory_stats(device)
        with torch.no_grad():
            _ = model(dummy_input)
        mem_used = torch.cuda.max_memory_allocated(device) / (1024 * 1024)
    else:
        with torch.no_grad():
            _ = model(dummy_input)
        mem_after = process.memory_info().rss / (1024 * 1024)
        mem_used = mem_after - mem_before

    return {"memory_mb": round(mem_used, 2)}

