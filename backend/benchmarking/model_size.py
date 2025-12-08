import os
import json

def get_model_size(model_path: str = "backend\models\model_best.pth") -> dict:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    size_bytes = os.path.getsize(model_path)
    size_mb = size_bytes / (1024 * 1024)  
    return {"model_size_mb": round(size_mb, 2)}

