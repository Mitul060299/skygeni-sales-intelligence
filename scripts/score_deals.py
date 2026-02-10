#!/usr/bin/env python
"""
Score new deals with the trained risk model.

Usage:
    python scripts/score_deals.py --input data/raw/new_deals.csv --output outputs/risk_scores.csv
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import joblib
import pandas as pd

from config import MODEL_FEATURES, MODELS_DIR, SEGMENT_COLUMNS
from features.feature_engineering import engineer_risk_features
from features.segment_probabilities import calculate_segment_probabilities
from data.data_loader import add_temporal_features, prepare_target_variable


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Score deals with risk model")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to output CSV")
    return parser.parse_args()


def main() -> None:
    """Load model and score deals."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    df = pd.read_csv(input_path)
    if "created_date" in df.columns:
        df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    if "closed_date" in df.columns:
        df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")
    if "outcome" in df.columns:
        df = prepare_target_variable(df)
    df = add_temporal_features(df)

    segment_path = MODELS_DIR / "segment_probabilities.json"
    if segment_path.exists():
        with segment_path.open("r", encoding="utf-8") as handle:
            segment_probs = json.load(handle)
    else:
        print("[WARN] Segment probabilities not found; computing from input data")
        segment_probs = calculate_segment_probabilities(df, SEGMENT_COLUMNS)
    df_features = engineer_risk_features(df, segment_probs)

    model_path = MODELS_DIR / "risk_scoring_model.pkl"
    model = joblib.load(model_path)

    X = df_features[MODEL_FEATURES]
    df_features["loss_probability"] = model.predict_proba(X)[:, 1]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_features.to_csv(output_path, index=False)
    print(f"[OK] Risk scores saved to: {output_path}")


if __name__ == "__main__":
    main()
