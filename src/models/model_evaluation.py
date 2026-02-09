"""
Model evaluation utilities.
"""

from typing import Dict

import numpy as np
from sklearn.metrics import average_precision_score, classification_report, roc_auc_score


def evaluate_classifier(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> Dict[str, float]:
    """
    Evaluate classifier performance.

    Args:
        y_true: Ground truth labels.
        y_pred: Predicted labels.
        y_proba: Predicted probabilities for positive class.

    Returns:
        Dictionary with evaluation metrics.
    """
    roc_auc = roc_auc_score(y_true, y_proba)
    avg_precision = average_precision_score(y_true, y_proba)
    report = classification_report(y_true, y_pred, output_dict=True)

    return {
        "roc_auc": roc_auc,
        "avg_precision": avg_precision,
        "precision_positive": report.get("1", {}).get("precision", 0.0),
        "recall_positive": report.get("1", {}).get("recall", 0.0),
    }
