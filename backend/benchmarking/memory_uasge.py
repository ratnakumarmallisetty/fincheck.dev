from model_loader import load_model

def model_memory():
    model, _ = load_model()

    total_params = sum(p.numel() for p in model.parameters())

    size_mb = total_params * 4 / (1024 * 1024)  # float32

    return {
        "parameters": total_params,
        "size_mb": size_mb
    }

if __name__ == "__main__":
    print(model_memory())
