from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data.data_loader import load_sales_data, prepare_target_variable


def test_load_sales_data(tmp_path: Path) -> None:
    data = pd.DataFrame(
        {
            "deal_id": ["D1"],
            "created_date": ["2024-01-01"],
            "closed_date": ["2024-01-10"],
            "sales_rep_id": ["R1"],
            "industry": ["Tech"],
            "region": ["NA"],
            "product_type": ["Core"],
            "lead_source": ["Inbound"],
            "deal_stage": ["Qualified"],
            "deal_amount": [10000],
            "sales_cycle_days": [9],
            "outcome": ["Won"],
        }
    )
    file_path = tmp_path / "sales.csv"
    data.to_csv(file_path, index=False)

    df = load_sales_data(file_path)
    assert len(df) == 1
    assert "created_date" in df.columns


def test_prepare_target_variable() -> None:
    df = pd.DataFrame({"outcome": ["Won", "Lost"]})
    df_target = prepare_target_variable(df)
    assert df_target["is_lost"].tolist() == [0, 1]
