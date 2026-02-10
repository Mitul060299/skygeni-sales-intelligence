# 🎯 SkyGeni Sales Intelligence Challenge
### Complete End-to-End Sales Analytics & AI System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **TL;DR:** Complete 5-part solution for SkyGeni Data Science / Applied AI Engineer challenge.
> Diagnoses declining B2B SaaS win rates, builds risk scoring system, and designs production architecture.
> Features custom RAPV metric revealing a 61.3% pipeline overestimation and an interpretable ML model for prioritized interventions.

---

## 📖 Project Overview

This repository contains my **complete submission** for the SkyGeni Sales Intelligence Challenge, covering all 5 required parts:

| Part | What It Covers | Key Deliverable | Where to Find |
|------|----------------|-----------------|---------------|
| **Part 1** | Problem Framing | Business problem definition, key questions, success metrics | [📄 docs/PART1_PROBLEM_FRAMING.md](docs/PART1_PROBLEM_FRAMING.md) |
| **Part 2** | Data Exploration & Insights | EDA, 3 business insights, 2 custom metrics (RAPV, REM) | [📄 docs/PART2_INSIGHTS_REPORT.md](docs/PART2_INSIGHTS_REPORT.md)<br>[📓 notebooks/01_EDA.ipynb](notebooks/01_EDA.ipynb)<br>[📓 notebooks/02_driver_analysis.ipynb](notebooks/02_driver_analysis.ipynb) |
| **Part 3** | Decision Engine | Deal risk scoring model with recommendations (experimental, gated deployment) | [📄 docs/PART3_DECISION_ENGINE.md](docs/PART3_DECISION_ENGINE.md)<br>[📓 notebooks/02_Deal_Risk_Scoring.ipynb](notebooks/02_Deal_Risk_Scoring.ipynb) |
| **Part 4** | System Design | Production architecture, API design, deployment strategy | [📄 docs/PART4_SYSTEM_DESIGN.md](docs/PART4_SYSTEM_DESIGN.md) |
| **Part 5** | Reflection | Assumptions, production risks, lessons learned, next steps | [📄 docs/PART5_REFLECTION.md](docs/PART5_REFLECTION.md) |

**👉 Start here for evaluation:** [docs/PART1_PROBLEM_FRAMING.md](docs/PART1_PROBLEM_FRAMING.md) → Then follow Parts 2-5 in sequence

---

## 📈 Business Impact Summary

| Metric | Value | Significance |
|--------|-------|--------------|
| **Pipeline Overestimation Discovered** | 61.3% gap (RAPV vs raw) | Corrects inflated revenue forecasts |
| **Potential Revenue Recovery** | $3,443,466 | From targeting 658 high-risk deals |
| **Model Performance** | 0.509 ROC-AUC | Interpretable baseline; not production-ready without gating |
| **High-Risk Deals Identified** | 658 deals (65.8% of scored set) | Focused intervention targets |
| **Custom Metrics Developed** | RAPV + REM | Better than traditional pipeline metrics |

---

## 🚀 Quick Navigation Guide

### For Reviewers / Evaluators

**→ To understand the business problem:**
1. Read [Part 1: Problem Framing](docs/PART1_PROBLEM_FRAMING.md) (10 min)

**→ To see the data analysis and insights:**
2. Read [Part 2: Insights Report](docs/PART2_INSIGHTS_REPORT.md) (15 min)
3. *Optional:* Open [01_EDA.ipynb](notebooks/01_EDA.ipynb) and [02_driver_analysis.ipynb](notebooks/02_driver_analysis.ipynb)

**→ To understand the ML solution:**
4. Read [Part 3: Decision Engine](docs/PART3_DECISION_ENGINE.md) (15 min)
5. *Optional:* Open [02_Deal_Risk_Scoring.ipynb](notebooks/02_Deal_Risk_Scoring.ipynb) for model details

**→ To see the production system design:**
6. Read [Part 4: System Design](docs/PART4_SYSTEM_DESIGN.md) (20 min)

**→ To understand limitations and learnings:**
7. Read [Part 5: Reflection](docs/PART5_REFLECTION.md) (10 min)

**Total review time: ~70 minutes** (or 30 minutes for just the docs, skipping notebooks)

---

### For Recruiters / Hiring Managers

**Quick assessment path (15 minutes):**
1. [Executive Summary](docs/PART1_PROBLEM_FRAMING.md#executive-summary) - Business problem definition
2. [Key Results Table](docs/PART2_INSIGHTS_REPORT.md#key-business-insights) - Business insights discovered
3. [Decision Engine Outputs](docs/PART3_DECISION_ENGINE.md#outputs) - What the system produces
4. [System Architecture Diagram](docs/PART4_SYSTEM_DESIGN.md#system-architecture-overview) - Production design
5. [Reflection](docs/PART5_REFLECTION.md) - Assumptions, risks, and lessons learned

---

### For Technical Deep Dive

**Want to run the code? (30 minutes):**

```bash
# 1. Clone repository
git clone https://github.com/Mitul060299/skygeni-sales-intelligence.git
cd skygeni-sales-intelligence

# 2. Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Option A: Run notebooks (interactive exploration)
jupyter notebook notebooks/
# → Open 01_EDA.ipynb for data exploration
# → Open 02_driver_analysis.ipynb for driver analysis
# → Open 02_Deal_Risk_Scoring.ipynb for model development

# 4. Option B: Run scripts (automated execution)
python scripts/run_eda.py                 # Runs exploratory analysis
python scripts/train_risk_model.py        # Trains risk scoring model
python scripts/score_deals.py --input data/raw/skygeni_sales_data.csv  # Scores deals
```

---

## 🧠 The Business Problem (Part 1)

**Context:**
A B2B SaaS company has **healthy pipeline volume** but **declining win rates** over two quarters.

**CRO's Question:**
"I don't know what exactly is going wrong or what my team should focus on."

**Our Answer:**
This is a **quality problem, not a quantity problem**. The issue is conversion efficiency, not lead generation.

**What We Built:**
1. **Diagnostic system** → Identifies *why* deals are being lost
2. **Predictive model** → Scores *which* deals are at risk now
3. **Recommendation engine** → Suggests *what actions* to take

**📄 Full details:** [Part 1: Problem Framing](docs/PART1_PROBLEM_FRAMING.md)

---

## 💡 Key Insights Discovered (Part 2)

### Insight #1: The Pipeline Optimism Gap
```
Raw Pipeline Value:     (reported pipeline)
Risk-Adjusted Value:    (RAPV forecast)
Optimism Gap:           61.3% overestimation
```
**Action:** Use RAPV (Risk-Adjusted Pipeline Value) for accurate forecasting

---

### Insight #2: Lead Source Quality Mismatch
```
Lead Source    Win Rate    Volume
────────────────────────────────
Inbound        46.0%       1,262 deals
Partner        43.95%      1,240 deals
Gap            2.1 pts     Equal effort, unequal results
```
**Action:** Shift marketing budget to Inbound, improve Partner qualification

---

### Insight #3: Sales Cycle Paradox
```
Correlation (Deal Size ↔ Sales Cycle): 0.021 ≈ ZERO
```
Small deals take as long as large deals = Process inefficiency
**Action:** Implement tiered sales processes by deal size

---

### Custom Metric #1: RAPV (Risk-Adjusted Pipeline Value)
```python
RAPV = Σ (Deal Amount × Segment Win Rate × Aging Penalty)
```
Weights pipeline by historical conversion rates per segment, with penalty for stalled deals.

### Custom Metric #2: REM (Revenue Execution Momentum)
```python
REM = (Win Rate × Avg Deal Size) / Avg Sales Cycle Days
```
Measures revenue generation efficiency (combines quality, size, and speed).

**📄 Full analysis:** [Part 2: Insights Report](docs/PART2_INSIGHTS_REPORT.md)
**📓 Interactive notebooks:** [01_EDA.ipynb](notebooks/01_EDA.ipynb), [02_driver_analysis.ipynb](notebooks/02_driver_analysis.ipynb)

---

## 🤖 The Decision Engine (Part 3)

Built an **interpretable ML model** that scores deals and recommends actions.

### What It Produces

**Input:** Deal characteristics (industry, source, amount, stage, cycle days)

**Output:**
```json
{
	"deal_id": "D12345",
	"risk_score": 78,
	"risk_category": "CRITICAL",
	"win_probability": "22%",
	"top_risk_factors": [
		"Partner lead source (-15 pts)",
		"Stuck in Qualified 42 days (-18 pts)",
		"EdTech industry (-8 pts)"
	],
	"recommended_actions": [
		"IMMEDIATE: Executive sponsor call",
		"THIS WEEK: ROI calculator + case study",
		"ONGOING: Weekly check-in"
	]
}
```

### Model Performance
| Metric | Value | Interpretation |
|--------|-------|----------------|
| ROC-AUC | 0.509 | Weak discrimination; experimental only |
| Precision (High Risk) | Varies by threshold | Tunable, but limited by signal |
| Interpretability | High | Segment-based probabilities + clear risk factors |

**Reality check:** Logistic Regression, Random Forest, Gradient Boosting, and XGBoost were tested and all scored near ~0.50 ROC-AUC. The weak signal appears driven by CRM data limitations rather than model choice or tuning, so automated deal-level prediction remains gated until stronger behavioral or engagement features are available.

**📄 Full methodology:** [Part 3: Decision Engine](docs/PART3_DECISION_ENGINE.md)
**📓 Model notebook:** [02_Deal_Risk_Scoring.ipynb](notebooks/02_Deal_Risk_Scoring.ipynb)

---

## 🏗️ Production System Design (Part 4)

Designed a complete architecture for deploying this system at scale.

### High-Level Architecture

```
┌─────────────┐
│ Salesforce  │  Daily sync (2 AM UTC)
│    CRM      │
└──────┬──────┘
			 │
			 ▼
┌──────────────────┐
│ Feature Pipeline │  Calculate RAPV, segment probabilities
└────────┬─────────┘
				 │
				 ▼
┌──────────────────┐
│  Risk Scorer     │  ML model inference (batch + real-time)
└────────┬─────────┘
				 │
				 ├─→ 🚨 Slack Alert (critical deals, <5 min)
				 ├─→ 📧 Daily Digest (managers, 8 AM local)
				 └─→ 📊 Dashboard (pipeline health, real-time)
```

### Key Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Data Ingestion | Airflow + Python | Nightly CRM sync with validation |
| Feature Engineering | pandas/numpy | Calculate RAPV, segment probs |
| Risk Scoring | scikit-learn + MLflow | Batch (100K deals/hour) + API (<200ms) |
| Alerts | Slack API + SendGrid | Critical alerts + daily digests |
| Dashboard | React + FastAPI | Pipeline health monitoring |
| Database | PostgreSQL + Redis | Structured data + caching |

### Production Considerations

✅ **Multi-tenant isolation (design)** - Row-level security with tenant_id
✅ **Model versioning (design)** - MLflow registry with rollback capability
✅ **Monitoring (design)** - Drift detection, calibration checks, performance tracking
✅ **Failure handling** - 8 scenarios documented with mitigation strategies
✅ **Scalability** - Handles 10-1,000 customers with auto-scaling

**📄 Complete specs:** [Part 4: System Design](docs/PART4_SYSTEM_DESIGN.md)

---

## 🎓 Learnings & Reflection (Part 5)

### Strengths and Gaps

**Strengths:**
- Identified the business problem (quality, not quantity)
- Developed useful custom metrics (RAPV, Deal Momentum)
- Built a transparent, interpretable system
- Documented model limitations explicitly

**Gaps:**
- Model performance is insufficient (0.509 ROC-AUC)
- Critical behavioral features are missing
- Recommendations are untested (no validation)
- The 20% intervention success rate is assumed

### Weakest Assumptions

1. **Data quality and completeness** - CRM data is clean, timely, and consistently logged
2. **Stable segment behavior** - Historical win rates remain reliable over time
3. **Comparable sales process** - Sales cycle and stage progression are standardized
4. **Model predictive accuracy** - CRM-only features are sufficient for prediction
5. **Intervention effectiveness** - Actions save 20% of at-risk deals

### What Would Break in Production

- CRM schema changes and field renames
- Concept drift in segment win rates
- Cold-start scenarios for new segments
- Alert fatigue from over-triggering
- Integration failures (API limits, auth, network)

### What I'd Build Next (1 month)

1. **Drift monitoring and retraining** - Calibration checks and automated retraining
2. **SHAP explainability** - Per-deal explanations and counterfactuals
3. **Feedback loop** - Track actions and measure outcomes
4. **Tenant onboarding toolkit** - Data quality checks and field mapping

**📄 Full reflection:** [Part 5: Reflection](docs/PART5_REFLECTION.md)

---

## 🛠️ Tech Stack

### Core Technologies

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)

### Production Stack (Part 4 Design)

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?logo=apache-airflow&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white)

---

## 📁 Repository Structure

```
skygeni-sales-intelligence/
│
├── 📊 data/
│   ├── raw/
│   │   └── skygeni_sales_data.csv          # Original dataset (5,000 deals)
│   └── processed/                           # Engineered features (generated)
│
├── 📓 notebooks/
│   ├── 01_EDA.ipynb                        # ⭐ Part 2: Exploratory analysis
│   ├── 02_driver_analysis.ipynb            # ⭐ Part 2: Driver analysis
│   └── 02_Deal_Risk_Scoring.ipynb         # ⭐ Part 3: Model development
│
├── 📖 docs/                                 # ⭐ Main deliverables (start here!)
│   ├── PART1_PROBLEM_FRAMING.md            # Part 1: Business problem definition
│   ├── PART2_INSIGHTS_REPORT.md            # Part 2: EDA insights & custom metrics
│   ├── PART3_DECISION_ENGINE.md            # Part 3: Risk scoring methodology
│   ├── PART4_SYSTEM_DESIGN.md              # Part 4: Production architecture
│   └── PART5_REFLECTION.md                 # Part 5: Learnings & limitations
│
├── 🔧 src/                                  # Production code modules
│   ├── __init__.py
│   ├── config.py                           # Configuration constants
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_loader.py                  # Data loading utilities
│   ├── features/
│   │   ├── __init__.py
│   │   ├── segment_probabilities.py        # RAPV calculation
│   │   └── feature_engineering.py          # Feature creation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── risk_scorer.py                  # Risk scoring model
│   │   └── model_evaluation.py             # Evaluation utilities
│   ├── recommendations/
│   │   ├── __init__.py
│   │   └── recommendation_engine.py        # Action generation
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                      # Helper functions
│
├── 🚀 scripts/                              # Executable scripts
│   ├── run_eda.py                          # Run exploratory analysis
│   ├── train_risk_model.py                 # Train risk scoring model
│   └── score_deals.py                      # Score new deals
│
├── ✅ tests/                                # Unit tests
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_feature_engineering.py
│   └── test_risk_scorer.py
│
├── outputs/                                 # Generated outputs
│   ├── figures/                            # Visualizations from EDA
│   └── reports/                            # Generated analysis reports
│
├── requirements.txt                         # Python dependencies
├── setup.py                                 # Package installation config
├── .gitignore
└── README.md                                # ⭐ You are here
```

### Key File Descriptions

**For evaluation, focus on:**
- `docs/PART*.md` - Complete written analysis for each part
- `notebooks/*.ipynb` - Interactive analysis (optional deep dive)

**For understanding implementation:**
- `src/` - Production-ready code modules
- `scripts/` - Executable entry points
- `tests/` - Validation tests

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_risk_scorer.py -v
```

---

## 📚 Complete Documentation Index

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [README.md](README.md) | Project overview & navigation | 10 min (this file) |
| [PART1_PROBLEM_FRAMING.md](docs/PART1_PROBLEM_FRAMING.md) | Business context, key questions, success metrics | 15 min |
| [PART2_INSIGHTS_REPORT.md](docs/PART2_INSIGHTS_REPORT.md) | EDA findings, 3 insights, 2 custom metrics | 20 min |
| [PART3_DECISION_ENGINE.md](docs/PART3_DECISION_ENGINE.md) | Risk scoring model, recommendations, examples | 20 min |
| [PART4_SYSTEM_DESIGN.md](docs/PART4_SYSTEM_DESIGN.md) | Production architecture, APIs, deployment | 25 min |
| [PART5_REFLECTION.md](docs/PART5_REFLECTION.md) | Assumptions, limitations, learnings | 10 min |

**Total reading time:** ~100 minutes for complete evaluation

---

## 🚀 Future Enhancements

### Phase 1 (Next 3 Months)
- [ ] Feedback loop to track intervention outcomes
- [ ] SHAP-based risk factor explanations
- [ ] Automated drift monitoring and alerting
- [ ] A/B testing framework for interventions

### Phase 2 (6-12 Months)
- [ ] Causal inference for risk factors
- [ ] Multi-touch attribution for sales actions
- [ ] Automated monthly model retraining
- [ ] Multi-vertical support (beyond B2B SaaS)

---

## 🐛 Known Limitations

**Data Limitations:**
- Training data limited to 15 months (seasonal patterns unknown)
- No competitor, pricing, or market context available
- Assumes CRM data is accurate and consistently logged

**Model Limitations:**
- Baseline ROC-AUC (0.509) prioritizes interpretability over accuracy
- Assumes stable segment behavior (drift detection is a planned capability)
- Intervention success rate (20%) is assumed, not measured

**System Limitations:**
- Multi-tenant isolation is a design target; production enforcement requires dedicated implementation and testing
- No A/B testing framework to validate interventions
- Alert thresholds need tuning to avoid fatigue

See [Part 5: Reflection](docs/PART5_REFLECTION.md) for detailed discussion.

---

## 👤 Author

**Mitul Srivastava**

📧 Email: srivastavamitul00@gmail.com
📱 Phone: +91 9582480350
💼 GitHub: [@Mitul060299](https://github.com/Mitul060299)

**Role:** Data Science / Applied AI Engineer Candidate
**Challenge:** SkyGeni Sales Intelligence System
**Submission Date:** 10 February 2026

---

## 🙏 Acknowledgments

- **SkyGeni** for the comprehensive and realistic challenge problem
- **scikit-learn** community for excellent ML tools
- **FastAPI** team for modern Python web framework design
- Sales intelligence platforms (Gong, Clari, SkyGeni) for inspiration

---

## 📄 License

This project is created for the SkyGeni Sales Intelligence Challenge.
Code is available under MIT License for educational purposes.

---

<div align="center">

**⭐ If this project demonstrates value, please consider starring the repository!**

Built with focus on **business impact**, **technical rigor**, and **production readiness**

[⬆ Back to Top](#-skygeni-sales-intelligence-challenge)

</div>
