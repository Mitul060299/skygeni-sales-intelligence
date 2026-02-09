#!/usr/bin/env python
"""
Script to run exploratory data analysis.

Usage:
    python scripts/run_eda.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import SALES_DATA_PATH
from data.data_loader import add_temporal_features, load_sales_data


def main() -> None:
    """Run basic EDA checks."""
    print("=" * 80)
    print("SKYGENI SALES INTELLIGENCE - EXPLORATORY DATA ANALYSIS")
    print("=" * 80)

    print("\nLoading data...")
    df = load_sales_data(SALES_DATA_PATH)
    df = add_temporal_features(df)

    print(f"[OK] Data loaded: {len(df):,} deals")
    print(f"Date range: {df['created_date'].min()} to {df['created_date'].max()}")

    print("\n" + "=" * 80)
    print("BASIC STATISTICS")
    print("=" * 80)
    print(df.describe())

    win_rate = (df["outcome"] == "Won").mean() * 100
    print(f"\nOverall Win Rate: {win_rate:.1f}%")
    print("\n[OK] EDA complete. Open notebooks/01_EDA.ipynb for details.")


if __name__ == "__main__":
    main()
