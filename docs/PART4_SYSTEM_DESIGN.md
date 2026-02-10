# SkyGeni Sales Intelligence - System Design
## Part 4: Production System Architecture

### Table of Contents
1. Executive Summary
2. Business Requirements
3. System Architecture Overview
4. Component Specifications
5. Data Flow & Processing
6. API Design
7. Alert & Notification System
8. Dashboard Design
9. Deployment Strategy
10. Monitoring & Observability
11. Failure Scenarios & Mitigation
12. Scalability Considerations
13. Security & Compliance
14. Cost Analysis
15. Success Metrics
16. Implementation Roadmap

## Executive Summary

This document describes the production architecture for SkyGeni's Sales Intelligence Platform - an AI-driven system that identifies at-risk deals and generates actionable recommendations for B2B SaaS sales teams.

**Problem Statement:**
B2B SaaS companies experience declining win rates despite healthy pipeline volume. Sales teams lack visibility into which deals are at risk and why, leading to missed revenue targets and inefficient resource allocation. The CRO needs a data-driven system to identify at-risk deals early and provide actionable intervention strategies.

**Solution:**
SkyGeni's Sales Intelligence Platform uses machine learning to predict deal risk, identify root causes, and recommend specific actions. The system combines historical segment performance (RAPV methodology from Part 2) with real-time deal characteristics to generate risk scores and targeted interventions.

**Key Capabilities:**
- Nightly batch scoring of all open deals (updated risk scores by 3 AM)
- Real-time risk assessment via API (<200ms response time)
- Automated alerts for critical deals (immediate Slack + email)
- Interactive dashboard for pipeline insights (RAPV, REM, trends)
- Recommendation engine with prioritized actions per deal

**Expected Impact:**
- Identify 658 high-risk deals in a 1,000-deal scored set (65.8%)
- Potential revenue recovery: ~$3.44M from targeted interventions
- Reduce time wasted on unsalvageable deals by 30%
- Provide data-driven prioritization for 50+ sales reps

## Business Requirements

### Functional Requirements

**FR1: Deal Risk Scoring**
- System must score all open deals with 0-100 risk score
- Risk categories: Low (0-25), Medium (26-50), High (51-75), Critical (76-100)
- Scores updated nightly at minimum (batch processing)
- On-demand scoring via API for urgent cases
- Risk scores include top 3 risk factors with impact quantification

**FR2: Alert System**
- **Critical deals (score >75)**: Immediate Slack + email alert to deal owner
- **High-risk deals (score 51-75)**: Included in daily digest (not immediate)
- Daily email digest to managers with top 10 high-risk deals (8 AM local time)
- Weekly executive summary to CRO with trends and recommendations

**FR3: Recommendation Engine**
- Each risk score includes top 3 risk factors with specific descriptions
- Prioritized action items per deal (immediate / this week / ongoing)
- Reference to similar deals that were successfully saved
- Customized recommendations based on deal characteristics

**FR4: Dashboard**
- Pipeline overview page (total value, RAPV, REM score, risk distribution)
- Deal list view (sortable by risk, amount, age, rep)
- Rep performance comparison (win rate, avg risk score of portfolio)
- Trend charts (win rate over time, deal volume, cycle time)
- Mobile-responsive design

**FR5: CRM Integration**
- Two-way sync with Salesforce (read deals, write risk scores)
- Risk score visible in Salesforce deal record as custom field
- Action items automatically create tasks in Salesforce
- Webhook support for real-time updates

### Non-Functional Requirements

**NFR1: Performance**
- API latency: <200ms (p95) for single deal scoring
- Batch processing: Complete within 60 minutes for up to 100K deals
- Dashboard load time: <2 seconds (initial page load)
- Database query response: <100ms (p95)

**NFR2: Reliability**
- System uptime: 99.5% (< 4 hours downtime/month)
- Data sync success rate: >99%
- Alert delivery: >99% (with retry mechanism)
- Graceful degradation if ML model unavailable

**NFR3: Scalability**
- Support 1,000 - 100,000 deals per customer
- Handle 10 - 1,000 customers on platform
- Auto-scale API tier during usage spikes
- Multi-tenant data isolation (schema-per-tenant or row-level security)

**NFR4: Security**
- SOC 2 Type II compliance ready
- Data encryption at rest (AES-256) and in transit (TLS 1.3)
- Role-based access control (RBAC) - Admin, Manager, Rep roles
- Audit logging for all data access and modifications
- API authentication via JWT tokens
- Tenant data isolation enforced at database and application layers

**NFR5: Usability**
- Dashboard accessible on desktop + mobile (responsive design)
- No training required (intuitive UI with tooltips)
- Alerts actionable with 1-click (deep links to deal records)
- Color-coded risk levels (red=critical, orange=high, yellow=medium, green=low)

## System Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  Web Dashboard  │  Mobile App  │  Slack Bot  │  Email Client       │
└────────┬────────────────┴──────────────┴──────────────┴─────────────┘
         │
         │ HTTPS / WebSocket
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│  AWS API Gateway / Kong                                             │
│  - Authentication (JWT validation)                                  │
│  - Rate limiting (100 req/min per user)                             │
│  - Request routing & load balancing                                 │
│  - API versioning enforcement                                       │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Dashboard   │  │  Risk Scorer │  │  Alert       │             │
│  │  API         │  │  Service     │  │  Service     │             │
│  │  (FastAPI)   │  │  (Python)    │  │  (Python)    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│         │                  │                  │                   │
│         └──────────────────┴──────────────────┘                   │
│                            │                                       │
│                   Multi-tenant context                             │
│                   (tenant_id in all queries)                       │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                     │
├─────────────────────────────────────────────────────────────────────┤
│  PostgreSQL (RDS)    │  Redis Cache   │  S3 Storage                │
│  - Deal records      │  - Feature     │  - Raw data snapshots      │
│  - Risk scores       │    vectors     │  - ML models (versioned)   │
│  - User data         │  - API cache   │  - Logs & backups          │
│  - Tenant metadata   │  - Session     │                            │
│                      │                │                            │
│  Row-level security: │                │                            │
│  WHERE tenant_id = ? │                │                            │
└────────┬─────────────────┴────────────────┴─────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  Apache Airflow / Prefect                                           │
│  - Daily CRM sync (per tenant, parallelized)                        │
│  - Feature engineering pipeline                                     │
│  - Batch scoring (tenant-isolated)                                  │
│  - Model retraining & versioning                                    │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   EXTERNAL INTEGRATIONS                             │
├─────────────────────────────────────────────────────────────────────┤
│  Salesforce  │  SendGrid  │  Slack  │  MLflow  │  Datadog          │
└─────────────────────────────────────────────────────────────────────┘
```

### Multi-Tenant Data Isolation

**Approach:** Row-level security with tenant_id column

**Implementation:**
```sql
-- All tables include tenant_id
CREATE TABLE deals (
    deal_id VARCHAR(50) PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    -- other columns
    CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);

-- RLS policy enforced at application layer
SELECT * FROM deals WHERE tenant_id = :current_tenant_id;

-- Database-level policy (PostgreSQL)
CREATE POLICY tenant_isolation ON deals
    USING (tenant_id = current_setting('app.current_tenant')::VARCHAR);

ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
```

**Alternative for scale:** Schema-per-tenant (future consideration)

### Technology Stack

**Infrastructure:**
- Cloud: AWS (primary)
  - Compute: ECS Fargate (containerized services)
  - Database: RDS PostgreSQL 14+ (Multi-AZ)
  - Cache: ElastiCache Redis 7+
  - Storage: S3 (Standard + Glacier for archival)
  - Orchestration: Managed Apache Airflow (MWAA)
- Containers: Docker
- CI/CD: GitHub Actions
- IaC: Terraform

**Data:**
- Database: PostgreSQL (with row-level security)
- Cache: Redis (with tenant-scoped keys)
- Storage: S3 (tenant prefix: s3://bucket/tenant_id/...)
- Message Queue: SQS (for async alert processing)

**Backend:**
- API: FastAPI (Python 3.11+)
- ML: scikit-learn 1.3+, MLflow 2.8+
- Data Processing: pandas 2.0+, NumPy
- Orchestration: Apache Airflow 2.6+

**Frontend:**
- Framework: React 18 + TypeScript
- Charts: Recharts / D3.js
- State: Redux Toolkit
- UI: Tailwind CSS + shadcn/ui
- Build: Vite

**Monitoring:**
- Logs: CloudWatch Logs
- Metrics: Prometheus + Grafana
- Alerts: PagerDuty
- APM: Datadog
- Error Tracking: Sentry

**Security:**
- Auth: Auth0 (with tenant context in JWT)
- Secrets: AWS Secrets Manager
- Encryption: AWS KMS

## Component Specifications

### 4.1 Data Ingestion Service

**Responsibility:** Extract deals from CRM, validate, and load to warehouse

**Technology:** Python + Apache Airflow

**Key Functions:**
```python
class CRMSyncService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.salesforce_client = SalesforceClient(tenant_id)

    def extract_deals(self, since: datetime) -> list:
        """Fetch deals from Salesforce API for specific tenant."""

    def validate_data(self, deals: list) -> dict:
        """
        Check schema, nulls, outliers.

        Validation Rules:
        - Required fields: deal_id, amount, created_date, stage
        - deal_amount must be > 0 and < $10M
        - created_date must be within last 5 years
        - No duplicate deal_ids within tenant
        """

    def transform_deals(self, deals: list) -> pd.DataFrame:
        """
        Normalize to standard format.

        Transformations:
        - Standardize industry names (e.g., "SaaS" vs "Software")
        - Parse dates to ISO format
        - Add tenant_id to all records
        - Calculate sales_cycle_days
        """

    def load_to_warehouse(self, df: pd.DataFrame) -> bool:
        """
        Upsert to database with tenant isolation.

        Uses INSERT ... ON CONFLICT UPDATE
        Ensures all records have tenant_id
        """
```

**DAG Schedule:**
```yaml
dag_id: daily_crm_sync_{{ tenant_id }}
schedule: "0 2 * * *"  # 2 AM UTC daily
retries: 3
retry_delay: 5m
timeout: 30m
concurrency: 10  # Max 10 tenants syncing simultaneously
on_failure: alert_ops_team
```

**Data Quality Checks:**
1. Schema validation (all required fields present)
2. Null check (deal_amount, created_date cannot be null)
3. Outlier detection (deal_amount >3 std dev flagged but not rejected)
4. Volume check (>20% drop from previous day -> alert, but continue)
5. Freshness (data updated in last 24 hours)
6. Duplicate check (no duplicate deal_ids within tenant)

**Failure Handling:**
- Salesforce API timeout -> Retry 3x with exponential backoff (2s, 4s, 8s)
- Schema change -> Halt pipeline for that tenant, alert engineering
- Volume anomaly -> Continue processing but flag for manual review
- Rate limit hit -> Queue for retry in 15 minutes

### 4.2 Feature Engineering Service

**Responsibility:** Calculate segment probabilities and engineer features

**Technology:** Python (pandas/numpy), cached in Redis

**Key Functions:**
```python
class FeatureEngineeringService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.cache = RedisCache(namespace=f"features:{tenant_id}")

    def calculate_segment_probabilities(self, historical_deals: pd.DataFrame) -> dict:
        """
        Calculate win rates by segment (industry, product, source, region).

        Cache TTL: 30 days (recalculated monthly)
        Minimum sample size: 10 deals per segment
        Fallback: Use overall win rate if <10 deals
        """

    def engineer_features(self, deal: Deal) -> FeatureVector:
        """
        Create feature vector for a single deal.

        Features:
        - Segment win probabilities (4 features)
        - Blended win probability (1 feature)
        - Deal size features (2 features: log_amount, is_large)
        - Sales cycle features (2 features: normalized_days, is_long)
        - Temporal features (2 features: is_q4, is_quarter_end)

        Total: 11 features
        """

    def batch_engineer_features(self, deals: list) -> pd.DataFrame:
        """
        Vectorized feature engineering for batch processing.

        Optimized for 10K+ deals (uses pandas operations)
        """
```

**Caching Strategy:**
```python
# Cache segment probabilities (recalculate monthly)
cache_key = f"segment_probs:{tenant_id}:{month}"
ttl = 30 * 24 * 60 * 60  # 30 days

# Cache individual deal features (recalculate daily)
cache_key = f"deal_features:{tenant_id}:{deal_id}"
ttl = 24 * 60 * 60  # 24 hours
```

**Edge Case Handling:**
- New industry not in training data -> Use overall average win rate
- Missing product type -> Default to 'Core' probability
- Outlier deal amount (>99th percentile) -> Cap at 99th percentile value
- Null sales cycle -> Use median for that industry

### 4.3 Risk Scoring Service

**Responsibility:** Predict deal loss probability using ML model

**Technology:** scikit-learn, MLflow (model registry)

**Key Functions:**
```python
class RiskScoringService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.model = self.load_model()
        self.feature_service = FeatureEngineeringService(tenant_id)

    def load_model(self) -> MLModel:
        """
        Load model from MLflow registry.

        Model Selection:
        1. Try tenant-specific model: models/{tenant_id}/production
        2. Fallback to global model: models/global/production
        3. Fallback to last-known-good model on registry failure

        Versioning: All models tagged with version (v1.0, v1.1, etc.)
        Rollback: Keep last 3 production models for quick rollback
        """
        try:
            model_uri = f"models:/{self.tenant_id}_risk_scorer/production"
            return mlflow.pyfunc.load_model(model_uri)
        except Exception as e:
            logger.warning(f"Tenant model not found, using global: {e}")
            return mlflow.pyfunc.load_model("models:/global_risk_scorer/production")

    def score_deal(self, deal: Deal) -> RiskScore:
        """
        Score a single deal (real-time API).

        Returns:
        - risk_score: 0-100 (higher = more risk)
        - risk_category: low/medium/high/critical
        - win_probability: 0-1
        - confidence: model confidence (0-1)
        """

    def batch_score_deals(self, deals: list) -> pd.DataFrame:
        """
        Score all deals for a tenant (nightly batch).

        Optimized for throughput:
        - Vectorized predictions
        - Batch size: 1000 deals at a time
        - Progress tracking for long-running jobs
        """

    def categorize_risk(self, risk_score: float) -> str:
        """
        Map risk score to category.

        Thresholds:
        - Low: 0-25 (>=75% win probability)
        - Medium: 26-50 (50-75% win probability)
        - High: 51-75 (25-50% win probability)
        - Critical: 76-100 (<25% win probability)
        """
```

**Model Versioning & Rollback:**
```yaml
# MLflow Model Registry Structure
models/
  - tenant_abc123/
    - production (alias -> version 3)
    - staging (alias -> version 4)
    - version 1 (archived)
    - version 2 (last-known-good)
    - version 3 (current production)

  - global/
    - production (fallback model)

# Rollback procedure (if model performance degrades):
1. Detect: Calibration error >10% for 3 consecutive days
2. Alert: Notify ML team via PagerDuty
3. Rollback: Promote version 2 to "production" alias
4. Verify: Check calibration on next batch run
5. Investigate: Root cause analysis on version 3
```

**Performance:**
- Single deal scoring: <40ms (model inference)
- Batch scoring: ~5 deals/second (on single CPU core)
- Parallel processing: 100+ deals/second (across 20 cores)

### 4.4 Recommendation Engine

**Responsibility:** Generate actionable recommendations based on risk factors

**Technology:** Python (rule-based system)

**Key Functions:**
```python
class RecommendationEngine:
    def identify_risk_factors(self, deal: Deal, model: MLModel, top_n: int = 3) -> list:
        """
        Identify top risk factors using feature importance.

        Uses SHAP values (if available) or model feature_importances_
        Returns factors with impact score and human-readable description
        """

    def generate_recommendations(self, risk_category: str, risk_factors: list, deal: Deal) -> list:
        """
        Map risk factors to specific actions.

        Rule-based mapping:
        - Long sales cycle -> Create timeline with milestones
        - Partner source -> Engage partner account manager
        - Low segment prob -> Provide case studies from that segment
        - Critical risk -> Executive sponsor involvement

        Priorities: immediate / this_week / ongoing
        """

    def find_similar_deals(self, deal: Deal, outcome: str = "won") -> list:
        """
        Find similar deals that were saved.

        Similarity criteria:
        - Same industry
        - Similar deal size (+/-30%)
        - Same risk factors
        - Successful outcome (won)

        Used for social proof in recommendations
        """
```

**Recommendation Rules (Examples):**
```python
# Rule: Long sales cycle
if "sales_cycle_days" in top_risk_factors:
    if deal.days_in_pipeline > 75:
        recommendations.append(Recommendation(
            priority="immediate",
            action="Create clear timeline with milestones and decision date",
            rationale=f"Deal has been open {deal.days_in_pipeline} days (avg: 63)"
        ))

# Rule: Partner lead source
if deal.lead_source == "Partner" and "lead_source" in top_risk_factors:
    recommendations.append(Recommendation(
        priority="this_week",
        action="Schedule joint call with partner account manager",
        rationale="Partner-sourced deals convert 2% lower; collaborative selling helps"
    ))

# Rule: Critical risk (any deal >75)
if risk_category == "critical":
    recommendations.append(Recommendation(
        priority="immediate",
        action="Escalate to VP Sales for executive sponsor involvement",
        rationale="Critical risk (<25% win probability) requires senior intervention"
    ))
```

### 4.5 Alert Dispatcher

**Responsibility:** Send alerts via Slack, email, and in-app notifications

**Technology:** Python, SendGrid (email), Slack API

**Key Functions:**
```python
class AlertDispatcher:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.sendgrid = SendGridClient()
        self.slack = SlackClient(tenant_id)

    def dispatch_critical_alert(self, deal: Deal, risk_score: RiskScore):
        """
        Send immediate alert for critical deals.

        Channels: Slack + Email (both sent immediately)
        Recipients: Deal owner + Manager
        Throttling: Max 1 alert per deal per 24 hours
        """

    def batch_daily_digest(self, manager_id: str, high_risk_deals: list):
        """
        Send daily digest email.

        Schedule: 8 AM in manager's timezone
        Content: Top 10 high-risk deals, trends, action items
        Throttling: Batched (not sent per-deal)
        """

    def send_weekly_summary(self, cro_email: str, metrics: PipelineMetrics):
        """
        Send executive summary.

        Schedule: Monday 9 AM
        Content: Win rate trend, RAPV, REM, top issues
        """
```

**Alert Timing Clarification:**

```markdown
### Alert Delivery Timing

**Critical Deals (risk score >75):**
- Timing: **Immediate** (< 5 minutes from score calculation)
- Mechanism: Event-driven (score change triggers SQS message)
- Channels: Slack + Email (parallel delivery)
- No batching for critical alerts
- Throttling: Max 1 alert per deal per 24 hours (prevents spam)

**High-Risk Deals (risk score 51-75):**
- Timing: **Batched** in daily digest (sent at 8 AM local time)
- Mechanism: Scheduled job queries high-risk deals
- Channels: Email only
- Batching interval: Once per day

**Medium/Low Risk Deals:**
- No automatic alerts
- Visible in dashboard only
- Can configure custom alerts (optional)

Example Flow:
1. Deal score increases from 68 -> 78 (crosses critical threshold)
2. Risk Scorer publishes event to SQS queue
3. Alert Dispatcher consumes event within seconds
4. Slack message sent immediately
5. Email sent immediately (in parallel)
6. Alert logged to prevent duplicate within 24h
```

## Data Flow & Processing

### Batch Processing Flow (Nightly)

**Timeline for 500 deals, single tenant:**

```
Time    | Component              | Action
--------|------------------------|------------------------------------------
02:00   | Airflow Scheduler      | Trigger daily_crm_sync_tenant_abc123 DAG
02:02   | CRM Sync Service       | Extract 500 deals from Salesforce (tenant: abc123)
02:05   | Data Validator         | Validate schema, quality checks
02:06   | Database               | Upsert deals table (WHERE tenant_id = 'abc123')
02:07   | Feature Service        | Load segment probabilities from cache
02:08   | Feature Service        | Engineer features for 500 deals (vectorized)
02:10   | Risk Scorer            | Load model from MLflow (tenant-specific or global)
02:11   | Risk Scorer            | Batch predict (500 deals, ~2 min @ 250/min)
02:13   | Database               | Update risk_scores table (tenant-scoped)
02:14   | Alert Generator        | Query deals WHERE risk_score > 75 AND tenant_id = 'abc123'
02:15   | Alert Generator        | Identify 12 new critical deals (score changed today)
02:16   | Alert Dispatcher       | Publish 12 events to SQS queue
02:17   | Alert Dispatcher       | Send 12 immediate Slack + email alerts
02:20   | Job Complete           | Update last_run timestamp for tenant
08:00   | Email Scheduler        | Send daily digest to 8 managers (batched)
```

**Multi-Tenant Orchestration:**

```yaml
# Airflow parallelizes across tenants
Tenant A sync: 02:00 - 02:20 ####################
Tenant B sync: 02:00 - 02:18 ################
Tenant C sync: 02:00 - 02:25 ######################
                                (runs in parallel)
```

### Real-Time Scoring Flow (API)

**Latency breakdown for single deal scoring:**

```
User Action: Sales rep clicks "Score This Deal" in Salesforce
    |
    +-> 1. Salesforce webhook -> API Gateway (50ms network)
    |
    +-> 2. API Gateway -> JWT validation -> Risk Scorer Service (10ms)
    |
    +-> 3. Risk Scorer checks Redis cache (5ms)
    |    - Cache hit -> Return cached score (total: 65ms)
    |    - Cache miss -> Continue to step 4
    |
    +-> 4. Query deal data from PostgreSQL (20ms)
    |    WHERE deal_id = :id AND tenant_id = :tenant
    |
    +-> 5. Load segment probabilities from Redis (5ms)
    |
    +-> 6. Engineer features (15ms - in-memory calculation)
    |
    +-> 7. Model inference (40ms - sklearn predict_proba)
    |
    +-> 8. Identify risk factors (10ms - feature importance)
    |
    +-> 9. Generate recommendations (15ms - rule engine)
    |
    +-> 10. Write to cache (tenant-scoped key) (5ms)
    |
    +-> 11. Return JSON response
    |
    +-> Total latency: ~185ms (within <200ms SLA)
```

### Data Retention Policy

```
Raw CRM Data (S3, tenant-prefixed):
s3://bucket/{tenant_id}/raw/...
- Last 90 days: Queryable (Standard storage)
- 90 days - 2 years: Archived (Glacier)
- >2 years: Deleted (compliance / GDPR)

Database (PostgreSQL, tenant-isolated):
deals table:
- Active deals: Full history (keep until deal closes)
- Closed deals: Last 2 years
- Purge: >2 years (GDPR right to deletion)

risk_scores table:
- Last 1 year: Full retention
- Purge: >1 year (historical scores not needed)

audit_logs table:
- Last 1 year: All actions logged
- Archive: >1 year to S3 Glacier
```

## API Design

### Base URL & Versioning

**Production:**
```
Base URL: https://api.skygeni.com
API Version: Included in path
Full endpoint: https://api.skygeni.com/v1/deals/score
```

**Staging:**
```
Base URL: https://api-staging.skygeni.com
```

**Versioning Strategy:**
- Version in path: /v1/, /v2/ (major versions only)
- Minor updates (backward-compatible): No version change
- Breaking changes: New major version (e.g., /v2/)
- Old versions supported for 12 months after deprecation notice

### Authentication

All endpoints require JWT token in Authorization header:

```http
Authorization: Bearer <jwt_token>
```

**Idempotency:**
POST requests accept an Idempotency-Key header to prevent duplicate writes on retries.

**JWT Claims:**
```json
{
  "sub": "user_123",
  "tenant_id": "abc123",
  "role": "manager",
  "exp": 1707648000
}
```

**Tenant Context:**
- Extracted from JWT tenant_id claim
- All database queries scoped: WHERE tenant_id = :tenant_id
- Cross-tenant access blocked at application layer

### Endpoints

#### POST /v1/deals/score

Score a single deal in real-time.

**Request:**
```json
{
  "deal_id": "D12345",
  "deal_amount": 45000,
  "industry": "EdTech",
  "product_type": "Enterprise",
  "lead_source": "Partner",
  "region": "North America",
  "created_date": "2026-01-15",
  "deal_stage": "Proposal",
  "sales_cycle_days": 28
}
```

**Response (200 OK):**
```json
{
  "deal_id": "D12345",
  "risk_score": 78,
  "risk_category": "critical",
  "win_probability": 0.22,
  "confidence": 0.85,
  "risk_factors": [
    {
      "factor": "Long sales cycle",
      "impact": 0.25,
      "description": "Deal has been open 28 days (avg: 14 for this segment)"
    },
    {
      "factor": "Partner lead source",
      "impact": 0.18,
      "description": "Partner leads convert 2% lower than Inbound"
    },
    {
      "factor": "EdTech industry",
      "impact": 0.12,
      "description": "EdTech win rate is 1.3% below average"
    }
  ],
  "recommendations": [
    {
      "priority": "immediate",
      "action": "Schedule executive sponsor call within 24 hours",
      "rationale": "Critical risk requires senior involvement"
    },
    {
      "priority": "this_week",
      "action": "Provide ROI calculator and EdTech case studies",
      "rationale": "Address industry-specific concerns"
    }
  ],
  "similar_deals": [
    {
      "deal_id": "D11234",
      "company": "Similar EdTech Co",
      "outcome": "won",
      "action_taken": "Executive sponsor call",
      "similarity_score": 0.89
    }
  ],
  "scored_at": "2026-02-11T10:30:00Z",
  "model_version": "v1.2.3"
}
```

**Error Responses:**
```json
{
  "error": "validation_error",
  "message": "Missing required field: deal_amount",
  "details": {
    "field": "deal_amount",
    "constraint": "required"
  }
}
```

```json
{
  "error": "unauthorized",
  "message": "Invalid or expired JWT token"
}
```

```json
{
  "error": "forbidden",
  "message": "Access denied: deal belongs to different tenant"
}
```

```json
{
  "error": "rate_limit_exceeded",
  "message": "Max 100 requests per minute exceeded",
  "retry_after": 30
}
```

```json
{
  "error": "internal_error",
  "message": "Model inference failed",
  "request_id": "req_abc123",
  "support_contact": "support@skygeni.com"
}
```

**Rate Limiting:**
- 100 requests per minute per user
- 1,000 requests per minute per tenant
- 429 response includes Retry-After header

#### GET /v1/deals/high-risk

Get list of high-risk deals for current user's tenant.

**Query Parameters:**
- risk_category (optional): Filter by category (high, critical, or both)
- limit (optional): Max results (default: 50, max: 200)
- offset (optional): Pagination offset (default: 0)
- sort_by (optional): Sort field (risk_score, amount, age)
- order (optional): asc or desc (default: desc)

**Example Request:**
```http
GET /v1/deals/high-risk?risk_category=critical&limit=10&sort_by=risk_score
Authorization: Bearer eyJ...
```

**Response:**
```json
{
  "deals": [
    {
      "deal_id": "D12345",
      "company": "Acme Corp",
      "amount": 45000,
      "risk_score": 82,
      "risk_category": "critical",
      "rep_name": "Jane Smith",
      "rep_id": "rep_5",
      "days_in_pipeline": 28,
      "current_stage": "Proposal",
      "last_activity": "2026-02-09T15:30:00Z"
    },
    {
      "deal_id": "D12346",
      "company": "Beta Inc",
      "amount": 32000,
      "risk_score": 79,
      "risk_category": "critical",
      "rep_name": "John Doe",
      "rep_id": "rep_12",
      "days_in_pipeline": 42,
      "current_stage": "Qualified",
      "last_activity": "2026-02-08T11:20:00Z"
    }
  ],
  "pagination": {
    "total_count": 47,
    "limit": 10,
    "offset": 0,
    "has_more": true
  },
  "summary": {
    "total_at_risk_revenue": 1230000,
    "average_risk_score": 76.3,
    "deals_by_category": {
      "critical": 25,
      "high": 22
    }
  }
}
```

#### GET /v1/pipeline/metrics

Get pipeline health metrics for current tenant.

**Response:**
```json
{
  "tenant_id": "abc123",
  "pipeline_value": 8200000,
  "risk_adjusted_value": 3700000,
  "optimism_gap": 4500000,
  "optimism_gap_pct": 54.9,
  "rem_score": 87380,
  "win_rate_pct": 45.3,
  "avg_sales_cycle_days": 63.2,
  "total_open_deals": 506,
  "risk_distribution": {
    "low": 228,
    "medium": 177,
    "high": 76,
    "critical": 25
  },
  "trend_indicators": {
    "win_rate_change_7d": 2.1,
    "rem_change_7d": -12.3,
    "avg_cycle_change_7d": 3.5
  },
  "as_of": "2026-02-11T02:00:00Z"
}
```

#### POST /v1/alerts/configure

Configure alert preferences for current user.

**Request:**
```json
{
  "critical_deals": {
    "enabled": true,
    "channels": ["slack", "email"],
    "threshold": 75
  },
  "daily_digest": {
    "enabled": true,
    "time": "08:00",
    "timezone": "America/New_York",
    "max_deals": 10,
    "min_risk_score": 51
  },
  "quiet_hours": {
    "enabled": true,
    "start": "20:00",
    "end": "08:00"
  }
}
```

**Response (200 OK):**
```json
{
  "user_id": "user_123",
  "settings_updated": true,
  "effective_at": "2026-02-11T10:35:00Z"
}
```

#### GET /v1/models/performance

Get model performance metrics (admin only).

**Response:**
```json
{
  "tenant_id": "abc123",
  "model_version": "v1.2.3",
  "deployed_at": "2026-02-01T00:00:00Z",
  "performance_metrics": {
    "roc_auc": 0.823,
    "precision_high_risk": 0.78,
    "recall_high_risk": 0.71,
    "calibration_error": 0.034,
    "f1_score": 0.745
  },
  "prediction_distribution": {
    "low": 0.45,
    "medium": 0.35,
    "high": 0.15,
    "critical": 0.05
  },
  "drift_metrics": {
    "feature_drift_score": 0.12,
    "prediction_drift_score": 0.08,
    "alert_status": "healthy"
  },
  "last_retrained": "2026-02-01T00:00:00Z",
  "next_retrain_scheduled": "2026-03-01T00:00:00Z"
}
```

## Alert & Notification System

### Alert Types

#### 1. Critical Deal Alert (Real-time)

**Trigger:** Deal risk score increases to >75
**Frequency:** Immediate
**Recipients:** Deal owner + manager
**Channels:** Slack + Email
**Priority:** High

**Slack Message Format:**
```
CRITICAL DEAL ALERT

Deal: Acme Corp - $45K
Risk Score: 82/100 (CRITICAL)

Top Risk Factors:
- Partner lead source (low conversion)
- Stuck in Qualified for 45 days
- EdTech industry (below-average win rate)

Recommended Actions:
- Schedule exec sponsor call within 24 hours
- Provide ROI calculator + case studies

[View Deal] [Snooze Alert] [Mark False Alarm]
```

**Email Subject:** "URGENT: High-risk deal - Acme Corp ($45K)"

#### 2. Daily Digest (Batch)

**Trigger:** Completion of nightly scoring
**Frequency:** Daily at 8 AM (recipient's timezone)
**Recipients:** Sales managers
**Channel:** Email

**Template:**
```html
<h2>Daily Pipeline Health Report</h2>
<p>Tuesday, February 11, 2026</p>

<h3>Pipeline Overview</h3>
<ul>
  <li>Scored Deals: 1,000 (latest batch)</li>
  <li>High/Critical Risk: 658 (65.8%)</li>
  <li>Potential Revenue Recovery: $3,443,466</li>
  <li>RAPV Gap: 61.3% (see Part 2 for pipeline diagnostics)</li>
</ul>

<h3>Deals Needing Attention (Top 5)</h3>
<table>
  <tr><td>1. Acme Corp</td><td>$45K</td><td>82/100 risk</td></tr>
  <tr><td>2. Beta Inc</td><td>$32K</td><td>79/100 risk</td></tr>
</table>

<h3>Trends This Week</h3>
<ul>
  <li>Lead source win-rate gap: 2.1 pp (Inbound vs Partner)</li>
  <li>Average deal cycle: (live)</li>
</ul>

<a href="https://dashboard.skygeni.com">View Full Dashboard</a>
```

### Alert Configuration

**User Preferences:**
```json
{
  "user_id": "manager_123",
  "alert_settings": {
    "critical_deals": {
      "enabled": true,
      "channels": ["slack", "email"],
      "threshold": 75
    },
    "daily_digest": {
      "enabled": true,
      "time": "08:00",
      "timezone": "America/New_York",
      "max_deals": 10
    },
    "quiet_hours": {
      "start": "20:00",
      "end": "08:00"
    }
  }
}
```

**Alert Throttling:**
- Critical alerts are immediate and never batched
- Max 1 critical alert per deal per day
- Daily digest includes high-risk deals only
- Respect quiet hours (no alerts 8 PM - 8 AM)

## Dashboard Design

### Core Views

**1. Pipeline Overview**
- Total pipeline value and risk-adjusted pipeline value
- RAPV, optimism gap, and REM score
- Risk distribution by category

**2. Deal Risk Table**
- Sortable by risk score, amount, days in pipeline
- Inline explanation (top 3 risk factors)
- One-click actions (create task, notify manager)

**3. Rep Performance**
- Win rate by rep and segment
- Average cycle time
- High-risk deal count per rep

**4. Trends and Forecast**
- Weekly win rate trend
- Pipeline volume trend
- Model performance trend

### Information Architecture
- Left navigation: Overview, Deals, Reps, Alerts, Settings
- Top filters: Date range, region, segment, team
- Drill-down: Click deal to view risk breakdown and recommendations

### Wireframe (Text)
```
+---------------------------------------------------------------+
| Pipeline Overview     [Date Range] [Region] [Team]            |
+---------------------------------------------------------------+
| Pipeline Value: (live)  | RAPV: (live) | REM: (live)            |
+---------------------------------------------------------------+
| Risk Distribution | Win Rate Trend | Cycle Time Trend         |
+---------------------------------------------------------------+
| Deals Needing Attention (Top 10)                              |
| Deal | Amount | Risk | Days | Owner | Recommended Action      |
+---------------------------------------------------------------+
```

## Deployment Strategy

### Environments
- Dev: feature branches, synthetic data
- Staging: production-like data with limited access
- Prod: audited access, strict change controls

### CI/CD
- GitHub Actions: unit tests, linting, build Docker images
- Security scanning: dependency and container scanning
- Automated deployments to staging, manual approval for prod

### Release Strategy
- Blue/green deployment for API services
- Canary releases for scoring model updates
- Rollback via previous Docker image and model version

## Monitoring & Observability

### Metrics
- API latency (p50, p95)
- Batch pipeline runtime
- Alert delivery success rate
- Model performance (ROC-AUC, precision-recall)
- Data drift indicators

### Logging
- Structured logs with request_id and deal_id
- Separate audit logs for admin actions
- Retention: 30 days hot, 1 year cold

### Alerts
- API error rate > 2% (5 min)
- Batch job runtime > 60 minutes
- Data drift detected for critical features
- Missing CRM sync for > 24 hours

## Failure Scenarios & Mitigation

| Scenario | Impact | Detection | Mitigation |
|---|---|---|---|
| CRM API outage | No new data | Airflow job failure | Retry with backoff, notify ops |
| Schema change in CRM | Pipeline failure | Validation error | Halt job, alert engineering |
| Model registry unavailable | No scoring | Health check failure | Serve last cached model |
| Redis cache down | Latency increase | Cache error rate | Fall back to DB, auto-recover |
| Slack API rate limit | Alert delay | Delivery failure | Queue retries, fallback to email |

## Scalability Considerations

- Horizontal auto-scaling on API and scoring services
- Partition risk_scores table by customer_id
- Precompute segment statistics nightly for large customers
- Use read replicas for dashboard queries
- Batch inference using chunking to avoid memory pressure

## Security & Compliance

- RBAC with least-privilege roles (rep, manager, admin)
- Encrypt data in transit (TLS 1.3) and at rest (KMS)
- Secrets stored in AWS Secrets Manager
- Audit logs for scoring requests and alert actions
- Data retention aligned with SOC 2 and customer contracts

## Cost Analysis

### Monthly Cost Estimate (Single Region)

| Component | Estimated Cost | Notes |
|---|---|---|
| RDS PostgreSQL | $450 | db.t3.medium + storage |
| ECS/Fargate | $700 | 3 services for API + jobs |
| Redis | $150 | cache.t3.small |
| S3 + Glacier | $120 | data + model artifacts |
| Airflow (MWAA) | $300 | managed or self-hosted |
| Monitoring | $200 | Datadog + CloudWatch |
| Total | $1,920 | baseline, scales with usage |

**Cost Trade-offs:**
- Start with a single-region setup; add multi-region when enterprise customers require it.
- Use reserved instances after usage stabilizes.

## Success Metrics

- 20% reduction in high-risk deal loss rate
- 10% increase in pipeline predictability (forecast accuracy)
- > 60% weekly active usage by sales managers
- < 2 second dashboard load time
- < 200ms p95 scoring API latency

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- CRM sync service and data validation
- Feature engineering library
- Basic batch scoring and alerts

### Phase 2: Productization (Weeks 5-8)
- Real-time scoring API
- Dashboard MVP
- Recommendation engine v1

### Phase 3: Reliability and Scale (Weeks 9-12)
- Monitoring, alerting, and data drift detection
- RBAC and audit logs
- Load testing and auto-scaling

### Phase 4: Optimization (Weeks 13-16)
- Model retraining automation
- A/B testing for recommendations
- Cost optimization and multi-region readiness
