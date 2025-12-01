import torch
from fvcore.nn import FlopCountAnalysis
from model_loader import load_model

def calculate_flops():
    model, device = load_model()
    dummy_input = torch.randn(1, 1, 28, 28).to(device)

    flops = FlopCountAnalysis(model, dummy_input)

    return {
        "FLOPs": flops.total(),
        "FLOPs_M": flops.total() / 1e6
    }

if __name__ == "__main__":
    print(calculate_flops())
