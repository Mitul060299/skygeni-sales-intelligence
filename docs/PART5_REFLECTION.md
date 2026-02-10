# SkyGeni Sales Intelligence Challenge - Part 5: Reflection

**Author:** Mitul Srivastava  
**Date:** 10 February 2026  

---

## 1. What Assumptions in Your Solution Are Weakest?

### Assumption 1: Data Quality and Completeness

**The Assumption:** CRM data is clean, timely, and consistently logged across all reps and regions.

**Why It's Weak:** In practice, data quality varies:
- Missing or incorrect close dates
- Inconsistent stage names across teams
- Delayed CRM updates (weekly instead of daily)
- Incomplete deal records

**Impact if Wrong:** Feature engineering fails, risk scores become unreliable, alerts fire on stale data.

**Mitigation:** Data quality checks in ingestion pipeline, validate freshness, flag missing critical fields.

**Confidence:** Medium - CRM data quality is notoriously inconsistent

---

### Assumption 2: Stable Segment Behavior

**The Assumption:** Historical segment win rates (industry, product, source, region) remain stable.

**Why It's Weak:** Market conditions change rapidly:
- New competitors enter (EdTech win rate drops)
- Pricing changes affect deal mix
- Partner programs improve or decline
- Economic shifts impact all segments differently

**Impact if Wrong:** Risk scores become miscalibrated using outdated win rates, RAPV metric becomes inaccurate.

**Mitigation:** Monthly recalculation of segment probabilities, drift detection (>5% change triggers alert), automated retraining.

**Confidence:** Low-Medium - Market dynamics change frequently

---

### Assumption 3: Comparable Sales Process

**The Assumption:** Sales cycles and stage progression are standardized across all reps, regions, and deal types.

**Why It's Weak:** Processes vary significantly:
- Enterprise reps: longer, complex cycles
- SMB reps: faster, shorter stages  
- Different regions have different approval processes
- CRM logging discipline varies by rep

**Impact if Wrong:** "Long cycle" means different things for different reps (30 days SMB vs 120 days Enterprise).

**Mitigation:** Normalize features by rep/region baselines, use percentile ranks instead of absolute values.

**Confidence:** Medium - Process variation exists but manageable

---

### Assumption 4: Model Predictive Accuracy

**The Assumption:** The ML model can accurately predict deal outcomes from available CRM features.

**Why It's Weak:** 
- ROC-AUC: 0.509 (essentially random guessing, 0.50 = coin flip)
- All algorithms performed identically (Logistic Regression, Random Forest, Gradient Boosting, XGBoost)
- Enhanced feature engineering didn't improve performance

**Root Cause - Missing Critical Features:**
- No behavioral data (email open rates, call frequency)
- No engagement signals (meetings, content downloads)
- No stakeholder data (champion strength, multi-threading)
- No competitive context (other vendors, pricing)
- Only static attributes (industry, amount, cycle length)

**Why Features Matter More Than Algorithms:**
```
Great Algorithm + Weak Features = 0.509 (Poor)
Average Algorithm + Strong Features = >0.70 (Good)
```

**Assessment:**  
This model is not production-ready for automated decisions. It currently serves as:
- A consistent prioritization framework that reduces ad hoc judgment
- Transparent risk factor identification
- Probabilistic scoring with limited predictive value

**What Would Fix This:**  
Behavioral features from Outreach/SalesLoft/Gong (email engagement, call data, meeting frequency) to reach >0.70 ROC-AUC.

**Confidence:** Very low - Model performance is insufficient

---

### Assumption 5: Intervention Effectiveness

**The Assumption:** Recommended actions save 20% of at-risk deals.

**Why It's Weak:** 
- No validation data
- 20% is assumed, not measured
- Different actions may have different effectiveness

**Impact if Wrong:** ROI calculations overstated, resources wasted on ineffective recommendations.

**Mitigation:** A/B test interventions, track outcomes, measure which actions work.

**Confidence:** Low - Zero validation data

---

## 2. What Would Break in Real-World Production?

### CRM Schema Changes
**What Breaks:** New stages, renamed fields, custom configurations  
**How It Breaks:** Pipeline fails, feature engineering crashes, alerts stop firing  
**Mitigation:** Schema versioning, flexible field mapping, automated change detection

### Concept Drift
**What Breaks:** Win rates shift (new competitor, pricing changes)  
**How It Breaks:** Model miscalibrates, risk scores become inaccurate, already poor performance (0.509) gets worse  
**Mitigation:** Weekly calibration checks, monthly segment recalculation, automated retraining

### Cold-Start Problem
**What Breaks:** New customers with <6 months history, new industry verticals  
**How It Breaks:** Unreliable segment probabilities, high prediction variance  
**Mitigation:** Global fallback model, minimum sample thresholds (30+ deals), explicit confidence scoring

### Alert Fatigue
**What Breaks:** Too many alerts, deals already known to be lost, threshold too aggressive  
**How It Breaks:** Managers stop opening alerts, system loses credibility  
**Mitigation:** Personalized thresholds, daily digest (top 10 only), track click-through rates

### Integration Failures
**What Breaks:** Salesforce API rate limits, auth tokens expire, network issues  
**How It Breaks:** Batch jobs fail, risk scores not updated, stale dashboard  
**Mitigation:** Retry logic, queue failed syncs, fallback to cached data with staleness warning

---

## 3. What Would You Build Next (Given 1 Month)?

### Week 1: Drift Monitoring and Automated Retraining
**Why:** Critical for production stability  
**What:**
- Daily calibration checks (predicted vs actual)
- Weekly segment win rate monitoring (>5% change = drift)
- Automated retraining when drift detected
- MLflow model registry with versioning
- A/B test new model, automatic rollback if worse

### Week 2: SHAP-Based Explainability
**Why:** Essential for user trust  
**What:**
- Replace feature importance with SHAP values
- Per-deal explanations with contribution scores
- Counterfactual recommendations ("If cycle reduced to 45 days, risk drops 15 points")
- Confidence intervals on risk factors

**Example:**
```
Deal Risk: 78/100 (Critical)

Contributing Factors (SHAP):
+18 pts: Sales cycle 42 days longer than industry median
+15 pts: Partner lead source (vs Inbound)
+8 pts: EdTech industry (below-average win rate)

What Would Help:
- Reduce cycle to 45 days -> Risk drops to 63
- Get exec sponsor -> Risk drops to 58
```

### Week 3: Feedback Loop and Action Tracking
**Why:** Essential for validating recommendations  
**What:**
- Log which recommendations were taken
- Track outcomes (did deal convert?)
- Measure actual effectiveness vs assumed 20%
- A/B test interventions (intervention vs control)
- Refine recommendations based on proven effectiveness

### Week 4: Tenant Onboarding Toolkit
**Why:** Required for scalability  
**What:**
- Data quality dashboard (missing fields, outliers, inconsistencies)
- CRM field mapping tool (handle custom schemas)
- Guided setup flow (connect -> map -> validate -> configure -> launch)

---

## 4. What Part of Your Solution Are You Least Confident About?

### Least Confident: Recommendation Quality and Actionability

**The Problem:**  
Current recommendations are rule-based without validation:
- "If critical -> recommend exec sponsor call"
- "If Partner source -> engage partner manager"
- "If long cycle -> create timeline"

**Basis for Low Confidence:**

- No validation: There is no tracking of recommendation adoption or outcomes.
- Assumed effectiveness: The 20% save rate is unverified and could vary widely.
- Generic guidance: The same actions are applied across critical deals without context.
- No feedback loop: There is no mechanism to measure action impact or improve guidance.

**Comparison to Model Performance:**  
The model performance is low (0.509 ROC-AUC), but it is measurable and repeatable. Recommendation quality has not been measured, so its effectiveness is currently unknown.

**What Would Increase Confidence:**
- Track which recommendations are adopted
- Measure outcomes (win rate for intervention vs control)
- A/B test alternative actions
- Quantify effectiveness (e.g., "Executive call improves win rates by 35% in comparable deals")

**Rationale for Candor:**  
It would be easy to claim the recommendations work, but that would be unsupported without validation data. It is more accurate to state: "This is a reasonable first version based on sales best practices that requires real-world validation."

---

## Summary: Key Learnings

### Strengths:
- Identified the business problem (quality, not quantity)
- Developed useful custom metrics (RAPV, Deal Momentum)
- Built a transparent, interpretable system
- Documented model limitations explicitly

### Gaps:
- Model performance is insufficient (0.509 ROC-AUC)
- Critical behavioral features are missing
- Recommendations are untested (no validation)
- The 20% intervention success rate is assumed

### Lessons Learned:
1. Features matter more than algorithms; weak data limits modeling gains.
2. Production standards exceed proof-of-concept; 0.509 ROC-AUC is not deployable.
3. Validation is essential; effectiveness claims require measurement.
4. Candid limitations improve trust and decision-making.

### Next Time:
- Acquire behavioral data before model development
- Set a minimum performance threshold (>0.70 ROC-AUC)
- Build a feedback loop from day one
- Start with rule-based prioritization before claiming ML sophistication