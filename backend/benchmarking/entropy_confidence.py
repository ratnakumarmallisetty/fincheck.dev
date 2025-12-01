import torch
import torch.nn.functional as F
import math
from model_loader import load_model

def confidence_entropy():
    model, device = load_model()
    dummy_input = torch.randn(1, 1, 28, 28).to(device)

    with torch.no_grad():
        logits = model(dummy_input)
        probs = F.softmax(logits, dim=1)
        confidence, _ = torch.max(probs, dim=1)

        entropy = -torch.sum(probs * torch.log(probs + 1e-9))

    return {
        "confidence": confidence.item(),
        "entropy": entropy.item()
    }

if __name__ == "__main__":
    print(confidence_entropy())
