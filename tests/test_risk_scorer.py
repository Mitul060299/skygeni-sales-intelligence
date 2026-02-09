from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.risk_scorer import predict_loss_probability, train_model


def test_train_and_predict() -> None:
    X = pd.DataFrame({"f1": [0.1, 0.2, 0.3, 0.4], "f2": [1, 0, 1, 0]})
    y = pd.Series([0, 1, 0, 1])

    model = train_model(X, y, model_type="logistic_regression")
    probs = predict_loss_probability(model, X)

    assert len(probs) == len(X)
    assert all(0 <= p <= 1 for p in probs)
