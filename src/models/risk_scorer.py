"""
Risk scoring model utilities.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from config import MODEL_CONFIGS


@dataclass
class ModelArtifacts:
    """Container for model artifacts."""

    model: Any
    feature_columns: List[str]


def build_model(model_type: str) -> Any:
    """
    Build a model instance from configuration.

    Args:
        model_type: One of 'logistic_regression', 'random_forest', 'gradient_boosting'.

    Returns:
        Configured model instance.
    """
    if model_type == "logistic_regression":
        return LogisticRegression(**MODEL_CONFIGS[model_type])
    if model_type == "random_forest":
        return RandomForestClassifier(**MODEL_CONFIGS[model_type])
    if model_type == "gradient_boosting":
        return GradientBoostingClassifier(**MODEL_CONFIGS[model_type])
    raise ValueError(f"Unsupported model_type: {model_type}")


def train_model(
    X_train: pd.DataFrame, y_train: pd.Series, model_type: str
) -> Any:
    """
    Train a model for risk scoring.

    Args:
        X_train: Training features.
        y_train: Training labels.
        model_type: Model type string.

    Returns:
        Trained model.
    """
    model = build_model(model_type)
    model.fit(X_train, y_train)
    return model


def predict_loss_probability(model: Any, X: pd.DataFrame) -> List[float]:
    """
    Predict loss probabilities for deals.

    Args:
        model: Trained model.
        X: Feature matrix.

    Returns:
        List of loss probabilities.
    """
    return model.predict_proba(X)[:, 1].tolist()
