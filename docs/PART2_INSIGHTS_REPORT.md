# Part 2 - Insights Report

## Executive Summary

The EDA confirms the CRO concern: pipeline volume is healthy, but conversion efficiency has weakened. The analysis focuses on diagnosing where win rate drops are concentrated and which segments or behaviors predict risk.

Key outputs:
- 3 actionable business insights
- 2 custom metrics (RAPV and Deal Momentum Score)
- Recommended actions tied to each insight

## Dataset Overview

- Records: 5,000 historical deals
- Date range: Jan 2023 - Mar 2024
- Target: Outcome (Won/Lost)
- Core dimensions: Industry, Region, Product Type, Lead Source, Sales Rep

## Custom Metrics

### 1) Risk-Adjusted Pipeline Value (RAPV)

**Definition:**
$\text{RAPV} = \sum (\text{Deal Amount} \times \text{Segment Win Probability})$

**Why it matters:**
Raw pipeline value overstates reality when win rates vary by segment. RAPV gives leadership a truer forecast for revenue planning and resource allocation.

### 2) Deal Momentum Score

**Definition:**
$\text{Momentum} = \text{Win Rate} \times \left(\frac{1}{\text{Avg Sales Cycle Days}}\right)$

**Why it matters:**
Momentum captures both conversion quality and velocity. A segment can look healthy on win rate alone but still be dragging revenue if cycles are long.

## Key Business Insights

### Insight 1: Pipeline Overestimation (RAPV Gap)

**Finding:** Risk-adjusted pipeline value is ~55% lower than raw pipeline value.

**Why it matters:** The CRO is forecasting based on inflated pipeline. This creates false confidence and late-stage surprises.

**Recommended action:** Shift forecasting and coverage planning to RAPV, and set weekly pipeline reviews around RAPV trends rather than raw value.

### Insight 2: Lead Source Efficiency Gap

**Finding:** Partner-sourced leads show a ~4.5% lower win rate than inbound leads.

**Why it matters:** The funnel is healthy, but lead quality varies significantly. Rep time is being spent on lower-converting channels.

**Recommended action:** Tighten qualification for partner deals or reallocate enablement resources to improve partner conversion playbooks.

### Insight 3: Sales Cycle Inefficiency

**Finding:** Longer sales cycles do not correlate with higher deal size, but they do correlate with lower win rates.

**Why it matters:** Extended cycles are risk signals rather than value signals. Slower deals are not paying off in larger ACV.

**Recommended action:** Introduce “stalled deal” triggers and executive review for deals that exceed median cycle length.

## Supporting Visuals (from notebook)

The notebook includes:
- Win rate by segment (industry, region, product, lead source)
- RAPV vs raw pipeline comparison
- Momentum score ranking by segment
- Sales cycle distribution and correlation checks

## Business Takeaways

- The win rate problem is not a volume problem; it is an efficiency and mix problem.
- RAPV should replace raw pipeline value for forecasting.
- Long-cycle deals are cost centers unless actively de-risked.
- Lead source quality is a lever leadership can improve quickly.
