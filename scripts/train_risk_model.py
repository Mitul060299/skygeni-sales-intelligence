#!/usr/bin/env python
"""
Script to train the deal risk scoring model.

Usage:
    python scripts/train_risk_model.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from config import MODEL_FEATURES, RANDOM_STATE, SALES_DATA_PATH, MODELS_DIR
from data.data_loader import add_temporal_features, load_sales_data, prepare_target_variable
from features.feature_engineering import engineer_risk_features
from features.segment_probabilities import calculate_segment_probabilities
from models.model_evaluation import evaluate_classifier
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

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    model = train_model(X_train, y_train, model_type="gradient_boosting")

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)
    metrics = evaluate_classifier(y_test.values, y_pred, y_proba)
    print(
        "[OK] Holdout metrics - "
        f"ROC-AUC: {metrics['roc_auc']:.3f}, "
        f"Avg Precision: {metrics['avg_precision']:.3f}"
    )

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / "risk_scoring_model.pkl"
    joblib.dump(model, model_path)

    segment_path = MODELS_DIR / "segment_probabilities.json"
    with segment_path.open("w", encoding="utf-8") as handle:
        json.dump(segment_probs, handle, indent=2, sort_keys=True)

    print(f"[OK] Model trained and saved: {model_path}")
    print(f"[OK] Segment probabilities saved: {segment_path}")


if __name__ == "__main__":
    main()
