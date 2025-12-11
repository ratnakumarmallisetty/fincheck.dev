# benchmarking/metrics_manager.py
from backend.benchmarking.system_metrics import get_system_metrics
from backend.benchmarking.inference_metrics import get_inference_metrics
from backend.benchmarking.model_analysis import get_model_analysis
from backend.benchmarking.prediction_quality import get_prediction_quality


__all__ = ["collect_all_metrics"]


def collect_all_metrics(job_id, model=None, tensor=None, probabilities=None):
    """
    Unified metrics aggregator across all team members.
    """

    return {
        "job_id": job_id,

        # Mukesh – System Metrics
        "system_metrics": get_system_metrics(),

        # Vikas – Inference Metrics
        "inference_metrics": (
            get_inference_metrics(model, tensor)
            if model is not None and tensor is not None
            else None
        ),

        # Albert – Model Analysis
        "model_analysis": (
            get_model_analysis(model)
            if model is not None
            else None
        ),

        # Rathna – Prediction Quality
        "prediction_quality": (
            get_prediction_quality(probabilities)
            if probabilities is not None
            else None
        ),
    }
