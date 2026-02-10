"""
Feature engineering utilities for risk scoring.
"""

from typing import Dict, Optional

import numpy as np
import pandas as pd

from config import (
    DEAL_SIZE_BINS,
    DEAL_SIZE_LABELS,
    LARGE_DEAL_PERCENTILE,
    LONG_CYCLE_THRESHOLD,
    OVERALL_WIN_RATE,
    SEGMENT_COLUMNS,
)


def engineer_risk_features(
    df: pd.DataFrame,
    segment_probs: Dict[str, Dict[str, float]],
    overall_win_rate: Optional[float] = None,
) -> pd.DataFrame:
    """
    Create feature set for risk scoring model.

    Args:
        df: Raw DataFrame.
        segment_probs: Segment win rate lookups.

    Returns:
        DataFrame with engineered features.
    """
    df_features = df.copy()
    if overall_win_rate is not None:
        global_win_rate = overall_win_rate
    elif "outcome" in df_features.columns:
        global_win_rate = (df_features["outcome"] == "Won").mean()
    else:
        global_win_rate = OVERALL_WIN_RATE

    for segment_type, prob_dict in segment_probs.items():
        feature_name = f"win_prob_{segment_type}"
        mapped = df_features[segment_type].map(prob_dict)
        df_features[feature_name] = mapped.fillna(global_win_rate)

    prob_columns = [f"win_prob_{seg}" for seg in SEGMENT_COLUMNS]
    df_features["blended_win_prob"] = df_features[prob_columns].mean(axis=1)
    df_features["blended_risk_prob"] = 1 - df_features["blended_win_prob"]

    segment_cycle_columns = []
    for segment_type in SEGMENT_COLUMNS:
        median_cycle_map = df_features.groupby(segment_type)["sales_cycle_days"].median()
        median_col = f"median_cycle_{segment_type}"
        df_features[median_col] = df_features[segment_type].map(median_cycle_map)
        segment_cycle_columns.append(median_col)

    overall_median_cycle = df_features["sales_cycle_days"].median()
    segment_median_cycle = df_features[segment_cycle_columns].mean(axis=1)
    segment_median_cycle = segment_median_cycle.fillna(overall_median_cycle)
    cycle_denominator = df_features["sales_cycle_days"].replace(0, np.nan)
    aging_factor = (segment_median_cycle / cycle_denominator).clip(upper=1.0)
    df_features["aging_factor"] = aging_factor.fillna(1.0)
    df_features["rapv_aging_value"] = (
        df_features["deal_amount"] * df_features["blended_win_prob"] * df_features["aging_factor"]
    )

    rem_score = (df_features["blended_win_prob"] * df_features["deal_amount"]) / cycle_denominator
    df_features["rem_score"] = rem_score.fillna(0.0)

    df_features["deal_amount_log"] = np.log1p(df_features["deal_amount"])
    median_amount = df_features["deal_amount"].quantile(LARGE_DEAL_PERCENTILE / 100)
    df_features["is_large_deal"] = (df_features["deal_amount"] > median_amount).astype(int)

    mean_cycle = df_features["sales_cycle_days"].mean()
    df_features["sales_cycle_normalized"] = df_features["sales_cycle_days"] / mean_cycle
    df_features["is_long_cycle"] = (
        df_features["sales_cycle_days"] > LONG_CYCLE_THRESHOLD
    ).astype(int)

    df_features["is_q4"] = df_features["month"].isin([10, 11, 12]).astype(int)
    df_features["is_quarter_end"] = df_features["month"].isin([3, 6, 9, 12]).astype(int)

    df_features["deal_size_segment"] = pd.cut(
        df_features["deal_amount"],
        bins=DEAL_SIZE_BINS,
        labels=DEAL_SIZE_LABELS,
    )

    return df_features
