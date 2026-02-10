"""
Data loading utilities for SkyGeni Sales Intelligence.
"""

from pathlib import Path
from typing import List

import pandas as pd


def load_sales_data(filepath: Path, parse_dates: bool = True) -> pd.DataFrame:
    """
    Load sales data from CSV file.

    Args:
        filepath: Path to CSV file.
        parse_dates: Whether to parse date columns.

    Returns:
        DataFrame with sales data.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If required columns are missing.
    """
    required_columns: List[str] = [
        "deal_id",
        "created_date",
        "closed_date",
        "sales_rep_id",
        "industry",
        "region",
        "product_type",
        "lead_source",
        "deal_stage",
        "deal_amount",
        "sales_cycle_days",
        "outcome",
    ]

    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_csv(filepath)
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        missing_list = ", ".join(sorted(missing_cols))
        raise ValueError(f"Missing required columns: {missing_list}")

    if parse_dates:
        df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
        df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")

    return df


def prepare_target_variable(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create target variable for risk scoring (1 = Lost, 0 = Won).

    Args:
        df: DataFrame with 'outcome' column.

    Returns:
        DataFrame with 'is_lost' target variable.
    """
    df_copy = df.copy()
    df_copy["is_lost"] = (df_copy["outcome"] == "Lost").astype(int)
    return df_copy


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add temporal features from date columns.

    Args:
        df: DataFrame with date columns.

    Returns:
        DataFrame with additional temporal features.
    """
    df_copy = df.copy()
    if "created_date" not in df_copy.columns:
        raise ValueError("created_date column is required to add temporal features")
    df_copy["created_quarter"] = df_copy["created_date"].dt.to_period("Q")
    if "closed_date" in df_copy.columns:
        df_copy["closed_quarter"] = df_copy["closed_date"].dt.to_period("Q")
    df_copy["created_month"] = df_copy["created_date"].dt.to_period("M")
    df_copy["month"] = df_copy["created_date"].dt.month
    df_copy["days_of_week"] = df_copy["created_date"].dt.dayofweek
    return df_copy
