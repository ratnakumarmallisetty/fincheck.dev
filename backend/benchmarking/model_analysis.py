import torch

def get_model_analysis(model):
    """
    Returns:
    - FLOPs (approx)
    - Model size
    - Memory footprint
    """

    # Count parameters
    param_count = sum(p.numel() for p in model.parameters())
    model_size_mb = (param_count * 4) / (1024 * 1024)

    # FLOPs (rough estimate: 2 * params)
    approx_flops = param_count * 2

    return {
        "param_count": param_count,
        "model_size_mb": model_size_mb,
        "approx_flops": approx_flops,
        "memory_footprint_mb": model_size_mb,  # same for float32 weights
    }
