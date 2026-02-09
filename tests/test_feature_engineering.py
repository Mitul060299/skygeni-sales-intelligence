from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from features.feature_engineering import engineer_risk_features
from features.segment_probabilities import calculate_segment_probabilities


def test_engineer_risk_features() -> None:
    df = pd.DataFrame(
        {
            "deal_id": ["D1", "D2"],
            "outcome": ["Won", "Lost"],
            "industry": ["Tech", "Finance"],
            "product_type": ["Core", "Core"],
            "lead_source": ["Inbound", "Partner"],
            "region": ["NA", "EMEA"],
            "deal_amount": [10000, 20000],
            "sales_cycle_days": [30, 90],
            "month": [1, 12],
        }
    )
    segment_probs = calculate_segment_probabilities(df, ["industry", "product_type", "lead_source", "region"])
    df_features = engineer_risk_features(df, segment_probs)

    assert "blended_win_prob" in df_features.columns
    assert "rem_score" in df_features.columns
    assert "rapv_aging_value" in df_features.columns
    assert "deal_amount_log" in df_features.columns
    assert "is_long_cycle" in df_features.columns
