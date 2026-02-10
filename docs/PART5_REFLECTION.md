# Part 5 - Reflection

## Weakest Assumptions

- **Data quality and completeness:** The solution assumes CRM data is clean, timely, and consistent across teams. In practice, missing close dates, inconsistent stage names, or delayed updates would degrade feature quality and risk scores.
- **Stable segment behavior:** The model assumes segment win rates (industry, product, lead source, region) stay relatively stable. Major shifts in market conditions or product mix would make these priors stale.
- **Comparable sales process:** The scoring logic assumes sales cycles and stage progression are comparable across reps and regions. If processes differ materially, the same features may mean different outcomes.

## Model Performance Reality Check

Logistic Regression, Random Forest, Gradient Boosting, and XGBoost were tested.
All models achieved ROC-AUC scores close to ~0.50. Gradient Boosting performed
slightly better numerically (ROC-AUC ~0.509), but the difference is not
statistically meaningful. Even after additional feature engineering (interaction
features, relative features, percentile features, segment confidence features),
model performance did not improve significantly and in some cases became worse.

This weak performance indicates limited predictive signal in the available CRM
dataset. The issue appears to be data limitations rather than model choice or
tuning. The current feature set lacks behavioral and engagement-based signals
that typically drive deal outcomes.

This model should not be considered production-ready for automated deal-level
prediction. It is presented as an experimental analytical layer within a
broader decision intelligence system.

## What Would Break in Production

- **Schema or CRM workflow changes:** New stages, renamed fields, or custom CRM configurations could break ingestion, feature engineering, or alert routing.
- **Concept drift:** If win rates or sales cycles shift quickly, the model will miscalibrate and alerts will be noisy or late.
- **Cold-start for new tenants:** Sparse history can cause unreliable segment probabilities and weak recommendations unless there is a strong global fallback and clear confidence handling.
- **Alert fatigue:** Without careful tuning, managers could ignore alerts, especially if thresholds are too aggressive or if high-risk volumes spike.

## What I Would Build Next (1 Month)

- **Drift monitoring and retraining automation:** Add scheduled calibration checks, drift metrics, and automatic rollback to last-known-good models.
- **Better explainability:** Add SHAP-based explanations, human-readable factors, and confidence intervals to improve trust.
- **Tenant onboarding toolkit:** Data quality checks, automatic mapping of CRM fields, and a guided setup flow to reduce integration friction.
- **Feedback loop:** Capture outcomes of recommended actions (was a deal saved?) to refine recommendations and measure ROI.

## Least Confident Area

- **Recommendation quality and actionability:** The current rules are reasonable, but they are not validated with rep behavior or outcome feedback. The recommendations need real usage data to prove they drive better outcomes and to prioritize actions that actually change win rates.
