# SkyGeni Sales Intelligence Challenge - Part 1: Problem Framing

**Author:** Mitul Srivastava  
**Date:** 10 February 2026  
**Challenge:** Data Science / Applied AI Engineer Role

---

## Executive Summary

This document defines the business problem, key questions, success metrics, and assumptions for SkyGeni's Sales Intelligence system. The core insight: **the problem is conversion efficiency, not pipeline generation**. The CRO has sufficient deal volume but declining win rates, indicating a quality/execution issue rather than a demand problem.

**Key Takeaway:** We need a diagnostic system that identifies *why* deals are being lost and *what actions* can reverse the trend, not just a reporting dashboard.

---

## 1. What is the Real Business Problem?

### Problem Statement

The core business problem is **declining sales conversion efficiency**, not insufficient pipeline.

**What we know:**
- ✅ Pipeline volume is healthy (deal flow is adequate)
- ❌ Win rate has declined over two quarters
- ❓ Root cause is unclear

**Therefore, the real problem is:**
> **"Why are fewer deals converting to wins despite having sufficient pipeline, and what specific actions can reverse this trend?"**

### Why This Matters

This is a **quality problem, not a quantity problem**. The implications are significant:

| If it's a quantity problem | If it's a quality problem |
|----------------------------|---------------------------|
| → Invest in more marketing | → Fix conversion process |
| → Hire more SDRs | → Improve rep effectiveness |
| → Generate more leads | → Better qualify existing leads |
| → Expand top-of-funnel | → Optimize middle/bottom-of-funnel |

The CRO is experiencing the latter, which requires **diagnostic intelligence**, not just more volume.

### Potential Root Causes (Hypotheses to Test)

The win rate decline could stem from several factors:

**1. Deal Mix Degradation**
- Shift toward lower-converting industries (e.g., more EdTech, less FinTech)
- Increase in smaller deals (lower commitment = higher churn risk)
- More competitive markets where win rates are naturally lower

**2. Lead Quality Decline**
- Deterioration in specific lead sources (e.g., Partner referrals vs. Inbound)
- Looser qualification criteria at top-of-funnel
- Marketing channel shifts yielding lower-intent prospects

**3. Execution Issues**
- Rep performance variance (some reps declining while others stable)
- Longer sales cycles correlating with lower win rates
- Deals stalling at specific stages (e.g., Proposal, Negotiation)

**4. External Market Factors**
- Increased competition requiring stronger differentiation
- Pricing pressure reducing close rates
- Economic conditions making buyers more conservative

**5. Process/Structural Changes**
- CRM migration causing data inconsistencies
- Compensation plan changes affecting rep behavior
- Sales methodology updates not yet effective

**Goal:** The AI system must differentiate between these hypotheses using data.

---

## 2. What Key Questions Should an AI System Answer for the CRO?

An effective Sales Intelligence system must answer **diagnostic** and **prescriptive** questions, not just descriptive ones.

### Tier 1: Diagnostic Questions (What's happening?)

**Q1: Where is the win rate declining?**
- Which industries, regions, products, or lead sources are underperforming?
- Is the decline widespread or concentrated in specific segments?
- Are certain sales reps driving the overall decline?

**Q2: When did the decline start and what changed?**
- Can we pinpoint the quarter/month when performance shifted?
- Did deal mix change around that time?
- Were there any process or market changes?

**Q3: Are deals taking longer to close?**
- Has average sales cycle length increased?
- Are deals stalling at specific stages?
- Does longer cycle correlate with lower win rate?

**Q4: How is deal quality trending?**
- Is average deal size increasing or decreasing?
- Are we pursuing more "long-shot" deals?
- Has lead source distribution shifted?

### Tier 2: Risk Assessment Questions (What's at risk now?)

**Q5: Which current open deals are most at risk of being lost?**
- Can we predict loss probability for each open deal?
- What are the specific risk factors per deal?
- How much revenue is at risk in the current pipeline?

**Q6: Which deals should we prioritize for intervention?**
- What's the expected value of saving each at-risk deal?
- Which deals have the highest ROI for rep attention?
- Are there patterns in deals we've successfully saved before?

### Tier 3: Prescriptive Questions (What should we do?)

**Q7: What actions can improve win rates?**
- Should we adjust qualification criteria for certain lead sources?
- Do specific reps need coaching or support?
- Should we reallocate resources to higher-performing segments?

**Q8: What would "good" look like?**
- If we fix the identified issues, what win rate is achievable?
- What's the revenue impact of improving by X percentage points?
- What's the fastest path to recovery?

### Why These Questions Matter

Traditional BI dashboards show **what happened** (descriptive).  
SkyGeni's AI system should show **why it happened** (diagnostic) and **what to do** (prescriptive).

Example contrast:
```
❌ Traditional BI: "Win rate is 43% (down from 47%)"
✅ SkyGeni AI: "Win rate dropped because Partner-sourced EdTech deals
               (15% of pipeline) are converting at only 32%.
               Recommendation: Tighten Partner qualification or provide
               EdTech-specific case studies to reps."
```

---

## 3. What Metrics Matter Most for Diagnosing Win Rate Issues?

Not all metrics are equally important. Here are the **critical** vs **supporting** metrics:

### Critical Metrics (Primary Diagnostics)

**1. Win Rate (%)**
```
Win Rate = (Deals Won) / (Total Closed Deals) × 100
```
- **Why critical:** Direct measure of conversion efficiency
- **Segment by:** Industry, region, product, lead source, rep, time period
- **Target granularity:** Monthly or quarterly trends

**2. Win Rate by Segment**
```
Segment Win Rate = (Wins in Segment) / (Closed Deals in Segment) × 100
```
- **Why critical:** Identifies concentrated underperformance
- **Key segments:** Industry, product tier, lead source, geography, rep
- **What to look for:** Segments >5 percentage points below average

**3. Sales Cycle Length (Days)**
```
Cycle Length = (Close Date - Created Date)
```
- **Why critical:** Long cycles often correlate with low win rates
- **Analyze by:** Outcome (won vs lost), segment, deal size
- **Red flag:** If avg cycle for lost deals >> won deals

**4. Stage Conversion Rates**
```
Stage Conversion = (Deals Advanced) / (Deals at Stage) × 100
```
- **Why critical:** Identifies specific bottlenecks in the funnel
- **Stages to track:** Qualified → Demo → Proposal → Negotiation → Closed
- **Red flag:** <50% conversion at any stage

### Supporting Metrics (Contextual Understanding)

**5. Pipeline Volume & Composition**
- Total deal count (to confirm "healthy" claim)
- Total pipeline value (ACV)
- Deal mix by segment (detect shifts)

**6. Average Deal Size (ACV)**
```
Avg Deal Size = Total Pipeline Value / Total Deal Count
```
- **Why useful:** Smaller deals may have different dynamics
- **What to look for:** Trend toward smaller, riskier deals

**7. Deal Velocity**
```
Velocity = (Deals Closed per Week) / (Open Deals)
```
- **Why useful:** Measures how quickly pipeline moves
- **Red flag:** Declining velocity = stagnation

**8. Rep-Level Metrics**
- Individual win rates
- Deals per rep
- Average cycle per rep
- Portfolio mix per rep

### Metric Hierarchy

```
Win Rate (Primary KPI)
    ↓
├─ Win Rate by Segment (Diagnostic)
├─ Sales Cycle Length (Leading Indicator)
├─ Stage Conversion (Process Health)
└─ Deal Mix/Quality (Context)
```

**Rule:** Start with overall win rate, decompose into segments, then correlate with cycle length and stage performance.

---

## 4. What Assumptions Are Being Made?

### Data Assumptions

**Assumption 1: Data Completeness**
- All closed deals have recorded outcomes (won/lost)
- No systematic missing data (e.g., all reps logging consistently)
- Deal stages are populated for all deals

**Risk if wrong:** Missing data could bias win rate calculations  
**Mitigation:** Check for null values, validate record counts

**Assumption 2: Data Accuracy**
- Sales reps accurately record deal stages and outcomes
- Close dates reflect actual close, not admin entry dates
- Deal amounts reflect final ACV, not initial quotes

**Risk if wrong:** "Garbage in, garbage out" - insights will be misleading  
**Mitigation:** Cross-validate with finance data if available

**Assumption 3: Consistent Definitions**
- "Won" and "Lost" are clearly defined and applied uniformly
- Stage names are consistent across all reps
- Industries/regions are standardized (not free-text)

**Risk if wrong:** Comparing apples to oranges across segments  
**Mitigation:** Data profiling to check for inconsistencies

### Business Assumptions

**Assumption 4: Market Stability**
- No major economic shocks during the analysis period
- Competitive landscape relatively stable
- Product offerings haven't fundamentally changed

**Risk if wrong:** External factors may explain decline, not internal issues  
**Mitigation:** Qualitative input from sales leadership on market changes

**Assumption 5: Process Stability**
- CRM system hasn't changed (no migration mid-period)
- Sales methodology consistent across quarters
- Compensation plans stable (not incentivizing wrong behaviors)

**Risk if wrong:** Process changes could create artificial trends  
**Mitigation:** Interview stakeholders about any operational changes

**Assumption 6: Multi-Dimensional Business**
- Company operates across multiple industries (not single-vertical)
- Multiple regions and product tiers exist
- Sufficient deal volume per segment for statistical significance

**Risk if wrong:** Segmentation analysis may not be meaningful  
**Mitigation:** Check sample sizes before drawing segment-level conclusions

**Assumption 7: Currency Consistency**
- All deal amounts in same currency (e.g., USD)
- No currency conversion needed
- No inflation adjustment required

**Risk if wrong:** Deal size comparisons could be distorted  
**Mitigation:** Verify currency field in data

**Assumption 8: Representative Time Period**
- Two quarters is sufficient to establish a trend
- Seasonal effects are accounted for (e.g., Q4 vs Q1)
- Historical data is relevant to current state

**Risk if wrong:** Short-term fluctuation mistaken for structural decline  
**Mitigation:** Extend analysis to 4-6 quarters if data available

### Modeling Assumptions (for Part 3)

**Assumption 9: Segment Stability**
- Historical segment win rates predict future performance
- No fundamental shifts in segment dynamics
- Past patterns are indicative of future risk

**Risk if wrong:** Risk scoring model will be inaccurate  
**Mitigation:** Monthly recalibration of segment probabilities

**Assumption 10: Actionability of Insights**
- Identified issues are within team's control to fix
- Recommendations are feasible given resources
- Leadership will act on data-driven insights

**Risk if wrong:** Great analysis but no business impact  
**Mitigation:** Focus on actionable levers, not just interesting patterns

---

## Success Criteria

This problem framing will be successful if:

✅ **For the CRO:**
- Clearly understand *why* win rate declined (not just *that* it declined)
- Know *which* deals are at risk right now
- Receive *specific actions* to take (not vague advice)

✅ **For Sales Managers:**
- Identify which reps or segments need support
- Prioritize deals for intervention
- Measure effectiveness of actions taken

✅ **For Sales Reps:**
- Get early warning on at-risk deals
- Understand specific risk factors per deal
- Receive actionable next steps (not just risk scores)

---

## Constraints & Guardrails

**Time Constraint:** This is a time-boxed challenge (6-8 hours), not a multi-month project
- Focus on highest-impact insights
- Prioritize interpretability over complex modeling
- Use standard tools (scikit-learn, pandas) not cutting-edge ML

**Data Constraint:** Working with historical closed deals, not real-time CRM
- No live pipeline to score (will simulate)
- Limited feature set (no email engagement, call logs, etc.)
- Cannot validate recommendations with A/B tests

**Business Constraint:** Solution must be explainable to non-technical stakeholders
- Avoid black-box models
- Provide clear rationale for risk scores
- Recommendations must be specific and actionable

---

## Next Steps

Based on this problem framing:

**Part 2 (EDA):** Validate hypotheses through data exploration
- Check if win rate decline is real and significant
- Identify which segments are underperforming
- Detect changes in pipeline mix or sales cycle

**Part 3 (Decision Engine):** Build risk scoring model
- Predict which open deals are likely to be lost
- Identify specific risk factors per deal
- Generate prioritized recommendations

**Part 4 (System Design):** Architect production system
- Real-time risk scoring API
- Automated alerts for at-risk deals
- Dashboard for pipeline health monitoring

**Part 5 (Reflection):** Assess assumptions and limitations
- What would break in production?
- What are we least confident about?
- What would we build next?

---

## Conclusion

The real business problem is **conversion efficiency, not pipeline volume**. The CRO needs a system that:

1. **Diagnoses** why win rates are declining (segment analysis, trend detection)
2. **Predicts** which current deals are at risk (risk scoring model)
3. **Prescribes** specific actions to take (recommendation engine)

Success means moving from reactive reporting ("win rate dropped") to proactive intervention ("these 12 deals need executive sponsor calls this week").

The key is balancing analytical rigor with business pragmatism - insights must be accurate *and* actionable.

---

**Document Status:** ✅ Complete  
**Next:** Part 2 - Exploratory Data Analysis
