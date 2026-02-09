# 🎯 SkyGeni Sales Intelligence Platform
### AI-Driven Deal Risk Scoring and Revenue Recovery System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange.svg)](https://jupyter.org/)

> **TL;DR:** Built an ML system that ranks at-risk B2B SaaS deals and recommends interventions.
> It introduces RAPV (Risk-Adjusted Pipeline Value) to expose forecast inflation and prioritizes
> sales actions based on loss probability and key drivers.

---

## 📈 Project Impact

| Metric | Value | Impact |
|--------|-------|--------|
| **Pipeline Overestimation** | 55% gap (RAPV vs raw) | Forecasts corrected for realism |
| **Potential Revenue Recovery** | $3,443,466 | Savings from targeted interventions |
| **Risk Scoring Model** | 0.509 ROC-AUC | Interpretable baseline for prioritization |
| **Risk Coverage** | 658 high-risk deals | Focused manager attention |

---

## 🚀 Quick Start

### Option 1: View Insights (No Setup Required)
```bash
docs/PART2_INSIGHTS_REPORT.md
docs/PART3_DECISION_ENGINE.md
docs/PART4_SYSTEM_DESIGN.md
docs/PART5_REFLECTION.md
```

### Option 2: Run Notebooks (5 Minutes)
```bash
git clone https://github.com/Mitul060299/skygeni-sales-intelligence.git
cd skygeni-sales-intelligence
pip install -r requirements.txt
jupyter notebook notebooks/
```

### Option 3: Run Production Code (Full Experience)
```bash
pip install -e .
python scripts/run_eda.py
python scripts/train_risk_model.py
python scripts/score_deals.py --input data/raw/skygeni_sales_data.csv
```

---

## 🧠 The Problem

- A B2B SaaS company has healthy pipeline volume but declining win rates.
- CRO needs diagnostic clarity on what changed and what actions to take.
- The goal is a decision system, not just a model: insights, risk scoring, and interventions.

---

## 💡 The Solution

### Part 1: Business Framing
- Focus on conversion efficiency, not lead volume.
- Key questions: which segments are underperforming, where deals stall, and what actions change outcomes.
- Core metrics: win rate by segment, stage conversion, sales cycle, pipeline mix, ACV.

### Part 2: Custom Business Metrics

**RAPV (Risk-Adjusted Pipeline Value with Aging Penalty)**
```
RAPV = Σ (Deal Amount × Segment Win Rate × Aging Factor)
```
Adds an aging penalty for deals older than the segment median cycle.

**Revenue Execution Momentum (REM)**
```
REM = (Win Rate × Avg Deal Size) / Avg Sales Cycle Days
```
Measures revenue execution per day (conversion, magnitude, and speed).

### Part 3: Deal Risk Scoring Engine
- Interpretable classifier with segment priors and temporal signals.
- Outputs risk score (0-100), category, top drivers, and recommended actions.
- Enables managers to focus on critical and high-risk deals first.

### Part 4: Production System Design
- Batch + real-time scoring, alerting, and dashboards.
- Multi-tenant isolation, model versioning, and observability.
- Failure cases and recovery paths documented.

---

## 📊 Key Results

### Business Insights
- **Pipeline overestimation:** RAPV reveals a 55% optimism gap.
- **Lead source gap:** Partner leads convert worse than inbound.
- **Sales cycle inefficiency:** Longer cycles correlate with lower win rates, not higher ACV.

### Model Outputs
| Output | Description |
|--------|-------------|
| Risk Score | 0-100 loss probability rank |
| Risk Category | Low / Medium / High / Critical |
| Top Drivers | 3 strongest risk factors |
| Actions | Prioritized interventions |

---

## 🛠️ Tech Stack

### Data and ML
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange.svg)

### Production Design (Part 4)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

---

## 📁 Project Structure

```
skygeni-sales-intelligence/
│
├── 📊 data/
│   ├── raw/                     # Original CSV data
│   └── processed/               # Engineered features
│
├── 📓 notebooks/
│   ├── 01_EDA.ipynb             # Exploratory analysis
│   └── 02_Deal_Risk_Scoring.ipynb  # Model development
│
├── 🔧 src/                      # Production code
│   ├── config.py
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── recommendations/
│   └── utils/
│
├── 🚀 scripts/
│   ├── run_eda.py
│   ├── train_risk_model.py
│   └── score_deals.py
│
├── ✅ tests/
├── 📖 docs/                     # Detailed writeups by part
└── README.md
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📚 Documentation

- [Part 1: Problem Framing](docs/PART1_PROBLEM_FRAMING.md)
- [Part 2: Insights Report](docs/PART2_INSIGHTS_REPORT.md)
- [Part 3: Decision Engine](docs/PART3_DECISION_ENGINE.md)
- [Part 4: System Design](docs/PART4_SYSTEM_DESIGN.md)
- [Part 5: Reflection](docs/PART5_REFLECTION.md)

---

## 🚀 Future Enhancements

- Drift monitoring and automated retraining
- SHAP-based explanations for risk drivers
- Feedback loop for action effectiveness
- CRM onboarding automation and field mapping

---

## 🎓 What I Learned

- Translating CRO-level business questions into measurable metrics
- Designing decision systems, not just ML models
- Balancing interpretability with predictive performance
- Building an architecture that supports batch + real-time scoring

---

## 🐛 Known Issues and Limitations

- Training data is limited to historical CRM records without pricing or competitor context
- Segment win rates can drift in market shifts
- Recommendation rules need outcome feedback to validate impact

---

## 👤 Author

**Mitul Srivastava**

- Email: srivastavamitul00@gmail.com
- Phone: +91 9582480350
- GitHub: https://github.com/Mitul060299

---

## 🙏 Acknowledgments

- SkyGeni for the challenge prompt and evaluation framework
- Inspiration from modern revenue operations and sales intelligence practices

---

If this project is helpful, consider starring the repo.
