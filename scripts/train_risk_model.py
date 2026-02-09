#!/usr/bin/env python
"""
Script to train the deal risk scoring model.

Usage:
    python scripts/train_risk_model.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import joblib
import pandas as pd

from config import MODEL_FEATURES, SALES_DATA_PATH, MODELS_DIR
from data.data_loader import add_temporal_features, load_sales_data, prepare_target_variable
from features.feature_engineering import engineer_risk_features
from features.segment_probabilities import calculate_segment_probabilities
from models.risk_scorer import train_model


def main() -> None:
    """Train and save a gradient boosting risk model."""
    print("=" * 80)
    print("TRAIN DEAL RISK SCORING MODEL")
    print("=" * 80)

    df = load_sales_data(SALES_DATA_PATH)
    df = prepare_target_variable(df)
    df = add_temporal_features(df)

    segment_probs = calculate_segment_probabilities(df, ["industry", "product_type", "lead_source", "region"])
    df_features = engineer_risk_features(df, segment_probs)

    X = df_features[MODEL_FEATURES]
    y = df_features["is_lost"]

    model = train_model(X, y, model_type="gradient_boosting")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / "risk_scoring_model.pkl"
    joblib.dump(model, model_path)

    print(f"[OK] Model trained and saved: {model_path}")


if __name__ == "__main__":
    main()
