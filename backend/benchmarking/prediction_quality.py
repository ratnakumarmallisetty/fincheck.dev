import math

def get_prediction_quality(probabilities):
    """
    Computes:
    - Confidence score (max probability)
    - Entropy of prediction
    """

    confidence = max(probabilities)

    # entropy = -sum(p log p)
    entropy = -sum(p * math.log(p + 1e-12) for p in probabilities)

    return {
        "confidence_score": confidence,
        "entropy": entropy,
    }
