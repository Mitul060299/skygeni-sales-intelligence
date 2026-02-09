# Part 3 - Decision Engine (Option A: Deal Risk Scoring)

## Problem Definition

Build a decision engine that scores open deals by probability of loss, explains the main risk drivers, and generates actionable recommendations for sales leaders.

**Input:** Current pipeline deals with standard CRM fields
**Output:** Risk score (0-100), risk category, top risk factors, and recommended actions

## Approach Summary

- Train a classification model on historical won/lost deals
- Engineer features from Part 2 insights (segment win rates, timing signals)
- Convert loss probabilities to a risk score and category
- Generate recommendations based on top contributing factors

## Feature Set

Core features used by the model:
- Segment win probabilities (industry, product type, lead source, region)
- Blended win probability across segments
- Deal size signals (log deal amount, large deal flag)
- Sales cycle signals (normalized cycle length, long-cycle flag)
- Revenue Execution Momentum (REM)
- Temporal signals (Q4 flag, quarter-end flag)

## Model Selection

Models compared:
- Logistic Regression
- Random Forest
- Gradient Boosting (selected)

**Selected Model:** Gradient Boosting
**Primary Metric:** ROC-AUC

This model balanced predictive performance with interpretability, enabling clear ranking of risk factors without complex infrastructure.

## Outputs

For each deal, the engine produces:
- **Risk score:** 0-100 (higher = more likely to be lost)
- **Risk category:** Low, Medium, High, Critical
- **Top risk factors:** 3 most influential features
- **Recommendations:** Prioritized actions (immediate / this week / ongoing)

Example actions include:
- Executive sponsor escalation for critical risk
- ROI calculator + case studies for low win-rate segments
- Timeline and milestone creation for long-cycle deals

## How Sales Leaders Use This

- **Daily prioritization:** Managers focus on critical and high-risk deals first
- **Targeted coaching:** Reps get specific action recommendations, not generic alerts
- **Forecast accuracy:** Risk scores improve predictability of likely wins
- **Resource allocation:** Attention shifts from low-probability deals to salvageable ones

## Limitations

- Model quality depends on CRM data completeness and consistency
- Segment priors can drift over time without retraining
- Recommendation rules are not yet validated with outcome feedback

## Artifacts Generated

- Risk scores table for the pipeline
- Calibration and risk distribution plots
- Sample deal risk report with recommended actions

These are included in the notebook outputs and scripts for batch scoring.
