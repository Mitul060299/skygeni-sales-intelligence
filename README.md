# SkyGeni Sales Intelligence Challenge
## AI-Driven Deal Risk Scoring System

**Author:** Mitul Srivastava
**Role:** Data Science / Applied AI Engineer
**Date:** February 2026

---

## Project Overview

This project builds an AI-driven sales intelligence system for B2B SaaS companies to:
- Identify deals at risk of loss
- Understand win/loss drivers
- Generate actionable recommendations for sales teams

**Business Context:**
A B2B SaaS company experienced declining win rates despite healthy pipeline volume.
This system diagnoses root causes and prevents revenue leakage through early intervention.

---

## Key Results

### Part 2: Data Exploration & Insights
- **3 Critical Business Insights** identified:
	1. 55% pipeline overestimation (RAPV metric)
	2. 4.5% lead source efficiency gap
	3. Sales cycle inefficiency (no correlation with deal size)

- **2 Custom Metrics** developed:
	1. Deal Momentum Score (win rate x velocity)
	2. Risk-Adjusted Pipeline Value (RAPV)

### Part 3: Decision Engine
- **Risk Scoring Model**: 0.509 ROC-AUC
- **Business Impact**: $3,443,466 potential revenue recovery
- **Actionable Output**: Specific recommendations per deal

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Mitul060299/skygeni-sales-intelligence.git
cd skygeni-sales-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Usage

```bash
# Run EDA
python scripts/run_eda.py

# Train risk scoring model
python scripts/train_risk_model.py

# Score deals
python scripts/score_deals.py --input data/raw/new_deals.csv --output outputs/risk_scores.csv
```

### Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

---

## Project Structure

```
skygeni-sales-intelligence/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── data/
│   ├── raw/
│   │   └── skygeni_sales_data.csv
│   ├── processed/
│   │   └── .gitkeep
│   └── README.md
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Deal_Risk_Scoring.ipynb
│   ├── 02_driver_analysis.ipynb
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_loader.py
│   ├── features/
│   │   ├── __init__.py
│   │   ├── segment_probabilities.py
│   │   └── feature_engineering.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── risk_scorer.py
│   │   └── model_evaluation.py
│   ├── recommendations/
│   │   ├── __init__.py
│   │   └── recommendation_engine.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── models/
│   └── .gitkeep
├── outputs/
│   ├── figures/
│   │   └── .gitkeep
│   ├── reports/
│   │   ├── .gitkeep
│   │   └── eda_results.pkl
│   └── README.md
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_feature_engineering.py
│   └── test_risk_scorer.py
├── docs/
│   ├── PART1_PROBLEM_FRAMING.md
│   ├── PART2_INSIGHTS_REPORT.md
│   ├── PART3_DECISION_ENGINE.md
│   ├── PART4_SYSTEM_DESIGN.md
│   └── PART5_REFLECTION.md
└── scripts/
		├── run_eda.py
		├── train_risk_model.py
		└── score_deals.py
```

---

## Tech Stack

- **Python 3.10+**
- **Data Analysis**: pandas, numpy
- **Machine Learning**: scikit-learn
- **Visualization**: matplotlib, seaborn
- **Notebooks**: Jupyter

---

## Model Performance

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.509 |
| Precision (Lost) | 0.56 |
| Recall (Lost) | 0.70 |
| Calibration Error | TBD |

---

## Business Impact

- **Deals Analyzed**: 5,000 historical deals
- **High-Risk Deals Identified**: 658 (65.8%)
- **Potential Revenue Recovery**: $3,443,466
- **ROI**: TBD

---

## Documentation

Detailed documentation available in /docs:
- [Part 1: Problem Framing](docs/PART1_PROBLEM_FRAMING.md)
- [Part 2: Insights Report](docs/PART2_INSIGHTS_REPORT.md)
- [Part 3: Decision Engine](docs/PART3_DECISION_ENGINE.md)
- [Part 4: System Design](docs/PART4_SYSTEM_DESIGN.md)
- [Part 5: Reflection](docs/PART5_REFLECTION.md)

---

## Results Artifacts

Generated outputs are stored in outputs/:
- outputs/reports/eda_results.pkl (EDA summary artifact)
- outputs/reports/risk_scores.csv (scored deals with risk categories)

---

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

---

## Development Workflow

1. **EDA**: Explore data in notebooks/01_EDA.ipynb
2. **Modeling**: Develop models in notebooks/02_Deal_Risk_Scoring.ipynb
3. **Productionize**: Extract code to src/ modules
4. **Test**: Write tests in tests/
5. **Deploy**: Use scripts in scripts/ for production

---

## Key Features

### 1. Risk Scoring System
- Predicts deal loss probability (0-100 score)
- Categorizes as Low/Medium/High/Critical risk
- Identifies top risk factors per deal

### 2. Recommendation Engine
- Generates specific actions based on risk factors
- Prioritized by urgency (immediate/weekly/ongoing)
- Customized per deal characteristics

### 3. RAPV Metric
- Risk-Adjusted Pipeline Value
- Realistic revenue forecasting
- Segment-based probability weighting

---

## License

This project is created for the SkyGeni Sales Intelligence Challenge.

---

## Acknowledgments

- SkyGeni for the challenge opportunity
- Inspiration from modern RevOps and Sales Intelligence platforms

---

## Contact

Mitul Srivastava - srivastavamitul00@gmail.com - +91 9582480350
Project Link: https://github.com/Mitul060299/skygeni-sales-intelligence