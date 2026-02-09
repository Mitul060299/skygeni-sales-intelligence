"""
Configuration for SkyGeni Sales Intelligence.
"""

from pathlib import Path
from typing import Dict, Tuple

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

SALES_DATA_PATH = RAW_DATA_DIR / "skygeni_sales_data.csv"

RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

RISK_THRESHOLDS: Dict[str, Tuple[int, int]] = {
    "low": (0, 25),
    "medium": (26, 50),
    "high": (51, 75),
    "critical": (76, 100),
}

AVG_DEAL_VALUE = 26286
OVERALL_WIN_RATE = 0.453
INTERVENTION_SUCCESS_RATE = 0.20

DEAL_SIZE_BINS = [0, 5000, 15000, 30000, float("inf")]
DEAL_SIZE_LABELS = ["small", "medium", "large", "enterprise"]

LONG_CYCLE_THRESHOLD = 75
LARGE_DEAL_PERCENTILE = 50

MODEL_CONFIGS = {
    "logistic_regression": {
        "random_state": RANDOM_STATE,
        "max_iter": 1000,
        "class_weight": "balanced",
    },
    "random_forest": {
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": RANDOM_STATE,
        "class_weight": "balanced",
    },
    "gradient_boosting": {
        "n_estimators": 100,
        "max_depth": 5,
        "learning_rate": 0.1,
        "random_state": RANDOM_STATE,
    },
}

SEGMENT_COLUMNS = ["industry", "product_type", "lead_source", "region"]

MODEL_FEATURES = [
    "win_prob_industry",
    "win_prob_product_type",
    "win_prob_lead_source",
    "win_prob_region",
    "blended_win_prob",
    "rem_score",
    "deal_amount_log",
    "is_large_deal",
    "sales_cycle_normalized",
    "is_long_cycle",
    "is_q4",
    "is_quarter_end",
]

PLOT_STYLE = "whitegrid"
FIGURE_SIZE = (14, 6)
FONT_SIZE = 10

RISK_COLORS = {
    "low": "#06A77D",
    "medium": "#F77F00",
    "high": "#E63946",
    "critical": "#8B0000",
}
