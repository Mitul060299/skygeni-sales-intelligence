"""
Recommendation engine for deal risk scoring.
"""

from dataclasses import dataclass
from typing import Any, List

import numpy as np
import pandas as pd


@dataclass
class RiskFactor:
    """Risk factor details for a deal."""

    feature: str
    impact: float
    description: str


@dataclass
class Recommendation:
    """Action recommendation for a deal."""

    priority: str
    action: str
    rationale: str


def identify_risk_factors(
    deal_features: pd.Series, model: Any, feature_columns: List[str], top_n: int = 3
) -> List[RiskFactor]:
    """
    Identify top risk factors for a specific deal.

    Args:
        deal_features: Single deal's feature values.
        model: Trained model.
        feature_columns: List of feature names.
        top_n: Number of top factors to return.

    Returns:
        List of RiskFactor objects.
    """
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    else:
        importances = np.ones(len(feature_columns))

    pairs = sorted(zip(feature_columns, importances), key=lambda x: x[1], reverse=True)
    risk_factors: List[RiskFactor] = []

    for feature, importance in pairs[:top_n]:
        value = deal_features.get(feature)
        if feature.startswith("win_prob_"):
            segment_type = feature.replace("win_prob_", "")
            segment_value = deal_features.get(segment_type, "Unknown")
            segment_label = segment_type.replace("_", " ").title()
            description = f"{segment_label}: {segment_value} (win rate: {value:.2f})"
        elif feature == "is_long_cycle" and value == 1:
            cycle_days = deal_features.get("sales_cycle_days", 0)
            description = f"Long sales cycle ({cycle_days:.0f} days)"
        elif feature == "is_large_deal":
            amount = deal_features.get("deal_amount", 0)
            description = f"Deal size: ${amount:,.0f}"
        else:
            description = f"{feature}: {value}"

        risk_factors.append(
            RiskFactor(feature=feature, impact=float(importance), description=description)
        )

    return risk_factors


def generate_recommendations(
    risk_category: str, risk_factors: List[RiskFactor], deal_features: pd.Series
) -> List[Recommendation]:
    """
    Generate action recommendations based on risk level and factors.

    Args:
        risk_category: Risk category label.
        risk_factors: List of identified risk factors.
        deal_features: Deal's feature values.

    Returns:
        List of recommendations.
    """
    recommendations: List[Recommendation] = []

    if risk_category == "critical":
        recommendations.append(
            Recommendation(
                priority="immediate",
                action="Schedule executive sponsor call within 24 hours",
                rationale="Deal has <25% win probability and needs senior intervention",
            )
        )

    if risk_category in ["high", "critical"]:
        recommendations.append(
            Recommendation(
                priority="this_week",
                action="Provide ROI calculator and customer case studies",
                rationale="High-risk deals need a stronger value proposition",
            )
        )

    for factor in risk_factors:
        if "lead_source" in factor.feature and "Partner" in factor.description:
            recommendations.append(
                Recommendation(
                    priority="this_week",
                    action="Engage partner account manager for joint call",
                    rationale="Partner-sourced deals benefit from collaborative selling",
                )
            )
        if factor.feature == "is_long_cycle":
            cycle_days = deal_features.get("sales_cycle_days", 0)
            recommendations.append(
                Recommendation(
                    priority="immediate",
                    action="Create timeline with clear milestones and next steps",
                    rationale=f"Deal open {cycle_days:.0f} days (above average)",
                )
            )

    if risk_category in ["medium", "high", "critical"]:
        recommendations.append(
            Recommendation(
                priority="ongoing",
                action="Weekly check-in with decision maker",
                rationale="Regular engagement prevents deal stagnation",
            )
        )

    return recommendations
