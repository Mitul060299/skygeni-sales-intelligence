"""
Calculate segment-based win probabilities for RAPV metric.
"""

from typing import Dict, List

import pandas as pd


def calculate_segment_probabilities(
    df: pd.DataFrame, segment_columns: List[str]
) -> Dict[str, Dict[str, float]]:
    """
    Calculate historical win rates for each segment.

    Args:
        df: DataFrame with historical deals.
        segment_columns: Categorical columns to calculate rates for.

    Returns:
        Dictionary mapping segment types to win rate dictionaries.
    """
    segment_probs: Dict[str, Dict[str, float]] = {}

    for segment in segment_columns:
        win_rates = df.groupby(segment).apply(
            lambda x: (x["outcome"] == "Won").mean()
        )
        segment_probs[segment] = win_rates.to_dict()

    return segment_probs


def apply_segment_probabilities(
    df: pd.DataFrame, segment_probabilities: Dict[str, Dict[str, float]]
) -> pd.DataFrame:
    """
    Map segment win probabilities to each deal as features.

    Args:
        df: DataFrame to add probability features to.
        segment_probabilities: Pre-calculated segment win rates.

    Returns:
        DataFrame with probability features added.
    """
    df_with_probs = df.copy()

    for segment_type, prob_dict in segment_probabilities.items():
        feature_name = f"win_prob_{segment_type}"
        df_with_probs[feature_name] = df_with_probs[segment_type].map(prob_dict)

    return df_with_probs


def calculate_blended_probability(
    df: pd.DataFrame, segment_columns: List[str]
) -> pd.DataFrame:
    """
    Calculate blended win probability across all segments.

    Args:
        df: DataFrame with segment probability features.
        segment_columns: List of segment types.

    Returns:
        DataFrame with 'blended_win_prob' column added.
    """
    df_with_blend = df.copy()

    prob_columns = [f"win_prob_{seg}" for seg in segment_columns]
    df_with_blend["blended_win_prob"] = df_with_blend[prob_columns].mean(axis=1)
    df_with_blend["blended_risk_prob"] = 1 - df_with_blend["blended_win_prob"]

    return df_with_blend
