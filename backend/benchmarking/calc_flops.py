import os
import torch
from ptflops import get_model_complexity_info
from ..msgqueue.worker_models import SmallCNN

def load_model():
    backend_root = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(backend_root, "models", "model_best.pth")

    checkpoint = torch.load(model_path, map_location="cpu")

    if "student_state" in checkpoint:
        state_dict = checkpoint["student_state"]
    elif "model_state" in checkpoint:
        state_dict = checkpoint["model_state"]
    else:
        raise KeyError("No valid model weights found in the checkpoint.")

    model = SmallCNN(num_classes=10)
    model.load_state_dict(state_dict)
    model.eval()
    return model


def calculate_flops():
    """
    Calculates FLOPs using ptflops and returns result as JSON/dict.
    """
    model = load_model()
    input_res = (3, 224, 224)
    macs_str, params_str = get_model_complexity_info(
        model,
        input_res,
        as_strings=True,
        print_per_layer_stat=False,
        verbose=False
    )

    result = {
        "flops": macs_str,
        "params": params_str
    }

    return result

