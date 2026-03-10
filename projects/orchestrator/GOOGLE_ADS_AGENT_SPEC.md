# Google Ads Agent — Feature Specification

## Overview

An autonomous agent that manages Google Ads campaigns across multiple client accounts. Operates in phases: read data → analyze → propose changes → execute with approval.

**Primary Goal:** Optimize campaign performance (ROI, CPA, impression share) with minimal manual intervention.

**Scale:** Multi-client support (batch 5-10 clients per run for efficiency)

---

## Functional Requirements

### Phase 1: Data Ingestion & Analysis (Read-Only)

**Input:**
- Client list (account IDs, budget constraints, KPI targets)
- Campaign filters (active only, or include paused?)
- Date range (last 7/30/90 days)
- API credentials

**Process:**

1. **Authenticate** to Google Ads API
   - Use OAuth2 refresh token
   - Handle token refresh if expired
   - Log authentication success/failure

2. **Enumerate accounts and campaigns**
   ```
   For each client:
     → Fetch customer account ID
     → List all campaigns (filter by status if needed)
     → For each campaign:
        • Fetch metrics (impressions, clicks, cost, conversions, ROAS)
        • Fetch ad groups
        • Fetch ads (text, display, etc.)
        • Fetch keywords + bid status
   ```

3. **Collect Performance Data**
   - Date range: impressions, clicks, cost, conversions, conversion value
   - Conversion metrics: CPC, CPM, CTR, conversion rate, ROAS, CPA
   - Ad group performance breakdown
   - Keyword performance (high-impression low-conversion keywords?)

4. **Store Results**
   ```json
   {
     "client_id": "ABC123",
     "account_name": "Example Corp",
     "run_date": "2026-03-03",
     "campaigns": [
       {
         "campaign_id": "123456",
         "campaign_name": "Spring Sale",
         "status": "ENABLED",
         "budget": 5000.00,
         "metrics": {
           "impressions": 45000,
           "clicks": 1200,
           "cost": 3500.00,
           "conversions": 45,
           "conversion_value": 22500.00,
           "cpc": 2.92,
           "ctr": 2.67,
           "cpa": 77.78,
           "roas": 6.43
         },
         "ad_groups": [...],
         "keywords": [...]
       }
     ]
   }
   ```

**Output:**
- Structured campaign snapshots (JSON)
- Store in database for historical comparison
- Summary: # accounts fetched, # campaigns, total spend, total conversions

**Error Handling:**
- Invalid account ID → Log + skip that client
- API auth fails → Alert + pause agent
- Rate limit hit → Backoff 60s + retry
- Network timeout → Retry up to 3x, then log error

---

### Phase 2: Intelligent Analysis & Proposals

**Input:**
- Current campaign data (from Phase 1)
- Historical data (last 7/30/90 day trends)
- Client KPI targets (target CPA, ROAS, budget)

**Analysis Rules:**

**Rule 1: Low-Performing Ad Groups**
```
If: Ad group CTR < industry average - 20%
    AND spend > $500
    Then: Recommend pause or overhaul
```

**Rule 2: High-Impression, Low-Conversion Keywords**
```
If: Keyword impressions > 500 in period
    AND conversion rate < 0.5%
    AND spend > $100
    Then: Recommend lower bid or pause
```

**Rule 3: Budget Waste**
```
If: Campaign spend > 95% of budget before day 15 of month
    Then: Recommend lower daily budget or narrow targeting
```

**Rule 4: ROAS Opportunity**
```
If: Campaign ROAS < 2.0 (or client's target)
    AND has high-converting keywords
    Then: Recommend shift budget from low-ROAS to high-ROAS keywords
```

**Rule 5: Impression Share Opportunity**
```
If: Campaign impression_share < 50%
    AND budget available
    Then: Recommend increase bid or expand audience
```

**Proposal Output:**

```json
{
  "client_id": "ABC123",
  "proposed_changes": [
    {
      "type": "pause_ad_group",
      "campaign_id": "123456",
      "ad_group_id": "789",
      "ad_group_name": "Summer Deals",
      "reason": "CTR 0.8% vs avg 2.1%, spend $520 for 2 conversions (CPA $260)",
      "expected_impact": "Save $520/month, likely minimal impact (low performance)"
    },
    {
      "type": "lower_bid",
      "campaign_id": "123456",
      "keyword_id": "456",
      "keyword_text": "blue shoes clearance",
      "current_bid": 3.50,
      "recommended_bid": 1.50,
      "reason": "1000 impressions, 2 conversions (0.2% rate), high waste",
      "expected_impact": "Reduce waste by ~60%, expected cost reduction $300/month"
    },
    {
      "type": "increase_budget",
      "campaign_id": "654321",
      "campaign_name": "Winter Coat",
      "current_daily_budget": 100,
      "recommended_daily_budget": 150,
      "reason": "ROAS 8.2, hitting budget cap early, money left on table",
      "expected_impact": "Capture additional $1500/month revenue, +$300 spend"
    },
    {
      "type": "expand_keywords",
      "campaign_id": "123456",
      "recommended_keywords": ["blue shoes on sale", "discount blue shoes"],
      "reason": "Existing keyword 'blue shoes' has high CTR 3.2%, ROAS 7.1",
      "expected_impact": "Drive additional high-ROAS conversions"
    }
  ],
  "summary": {
    "total_proposals": 4,
    "estimated_monthly_savings": 820,
    "estimated_revenue_gain": 1500,
    "net_benefit": 680
  }
}
```

**Error Handling:**
- Insufficient historical data → Flag proposal as "low confidence"
- Client KPI targets missing → Use industry defaults (CPA avg, ROAS > 3)
- Zero conversions in period → Flag campaign, don't recommend changes yet

---

### Phase 3: Execution (With Approval)

**Input:**
- Approved proposals (from Phase 2)
- Approval log (which changes were greenlit by user/admin)

**Actions to Implement:**

1. **Pause Ad Group**
   ```
   API: UpdateAdGroup(status=PAUSED)
   Log: Old status, new status, timestamp
   Rollback: Can re-enable if needed within 48h
   ```

2. **Adjust Keyword Bid**
   ```
   API: UpdateKeyword(cpc_bid=new_value)
   Log: Old bid, new bid, reason
   Validation: Bid within platform limits (0.05 - 10000)
   Rollback: Store old bid, can restore
   ```

3. **Update Campaign Budget**
   ```
   API: UpdateCampaign(daily_budget=new_value)
   Log: Old budget, new budget
   Validation: Budget matches client limits
   Rollback: Store old budget, can restore
   ```

4. **Add Keywords**
   ```
   API: CreateKeyword(campaign_id, ad_group_id, keyword_text, bid)
   Log: Keyword added, bid, targeting
   Validation: Keyword not duplicate, matches ad group theme
   Rollback: Delete keyword if needed
   ```

**Execution Guardrails:**
- Max changes per client per day: 20 (prevent accidents)
- Pause no more than 30% of ad groups in a campaign
- Don't increase or decrease budget >20% in one day
- Never delete campaigns (pause only)
- Log every single change with reason + timestamp

**Execution Log:**
```json
{
  "execution_id": "exec-20260303-abc123",
  "client_id": "ABC123",
  "execution_time": "2026-03-03T14:32:45Z",
  "changes": [
    {
      "status": "success",
      "action": "pause_ad_group",
      "ad_group_id": "789",
      "api_response_time": "0.23s"
    },
    {
      "status": "success",
      "action": "adjust_bid",
      "keyword_id": "456",
      "old_bid": 3.50,
      "new_bid": 1.50
    },
    {
      "status": "failed",
      "action": "increase_budget",
      "campaign_id": "111",
      "error": "API rate limit exceeded",
      "retry_at": "2026-03-03T15:00:00Z"
    }
  ],
  "summary": {
    "succeeded": 2,
    "failed": 1,
    "pending_retry": 1
  }
}
```

**Error Handling:**
- API call fails → Immediately rollback if possible, log error, alert
- Partial success (some changes work, some fail) → Log clearly, retry failed ones
- Network timeout during execution → Wait + retry, don't double-execute

---

## Non-Functional Requirements

### Performance

- **Batch size:** 5-10 clients per run (optimize API calls)
- **Total run time:** <15 minutes per batch (includes data fetch + analysis)
- **Data freshness:** Run daily (morning)
- **Latency for individual requests:** <5s per API call

### Reliability

- **Uptime:** 99%+ (scheduled maintenance windows acceptable)
- **Retry logic:** 3 attempts per failed API call, exponential backoff
- **Failover:** If one client fails, continue with others
- **Data consistency:** Transaction-based (all-or-nothing for multi-step changes)

### Security

- **Credentials:** Never log API keys, store in vault only
- **Data exposure:** Sanitize logs (don't include client campaign names in public logs)
- **Access control:** Only read/write approved resources
- **Audit trail:** Every change logged with user/agent ID + timestamp

### Observability

- **Logging:** DEBUG (details) → INFO (key events) → ERROR (problems)
- **Metrics:** Execution time, success rate, API quota usage, # proposals vs approvals
- **Tracing:** Request ID for every agent run (track through logs)

---

## Input/Output Specifications

### Agent Input

```json
{
  "task": "Analyze and optimize Google Ads campaigns",
  "phase": 1,  // or 2, 3
  "clients": [
    {
      "customer_id": "ABC123",
      "account_name": "Example Corp",
      "budget_constraint": 50000,  // monthly
      "kpi_targets": {
        "target_cpa": 50,
        "target_roas": 4.0,
        "max_daily_budget": 2000
      }
    }
  ],
  "date_range": {
    "start": "2026-02-03",
    "end": "2026-03-03"
  },
  "api_credentials": {
    "vault_key": "google-ads-api-prod"
  }
}
```

### Agent Output (Phase 1)

```json
{
  "run_id": "run-20260303-001",
  "agent": "google-ads-manager",
  "phase": 1,
  "status": "success",
  "timestamp": "2026-03-03T14:00:00Z",
  "data": {
    "clients_processed": 8,
    "clients_failed": 0,
    "total_campaigns": 142,
    "total_spend": 45230.50,
    "total_conversions": 1850,
    "campaigns": [...]
  },
  "logs": {
    "info": ["Fetched 8 accounts", "Processed 142 campaigns"],
    "errors": []
  }
}
```

### Agent Output (Phase 2)

```json
{
  "run_id": "run-20260304-002",
  "agent": "google-ads-manager",
  "phase": 2,
  "status": "success",
  "timestamp": "2026-03-04T14:30:00Z",
  "proposals": [
    {
      "client_id": "ABC123",
      "changes": [...]
    }
  ],
  "summary": {
    "total_proposals": 12,
    "estimated_monthly_savings": 2340,
    "estimated_revenue_gain": 5600,
    "net_expected_benefit": 3260
  }
}
```

### Agent Output (Phase 3)

```json
{
  "run_id": "run-20260305-003",
  "agent": "google-ads-manager",
  "phase": 3,
  "status": "success",
  "timestamp": "2026-03-05T15:00:00Z",
  "execution_results": {
    "succeeded": 10,
    "failed": 2,
    "pending_retry": 1
  },
  "changes": [...]
}
```

---

## Dependencies

- **External APIs:** Google Ads API (v17+)
- **Libraries:** `google-ads-api-python-client`, `protobuf`, `requests`
- **Data:** Historical campaign data (persist in DB)
- **Secrets:** Google Ads OAuth2 credentials (refresh token)

---

## Success Metrics

**Phase 1:**
- ✅ Fetches all accounts without errors
- ✅ Data matches Google Ads UI
- ✅ Run completes in <10 minutes

**Phase 2:**
- ✅ Proposals are actionable (specific campaign/keyword/ad group IDs)
- ✅ Estimated impact is accurate (validate against actual results 2 weeks later)
- ✅ No false positives (rules don't recommend obviously bad changes)

**Phase 3:**
- ✅ Changes execute without errors
- ✅ Actual ROAS/CPA improves within 2 weeks
- ✅ Client satisfaction (approves >70% of proposals)
- ✅ ROI on agent effort is >10:1 (time saved + revenue gained vs agent cost)

---

## Known Limitations & Caveats

1. **Real-time changes:** Agent sees yesterday's data (API lag). Real-time optimization not possible yet.
2. **Cross-campaign optimization:** Doesn't optimize across campaigns (might move budget between campaigns). Phase 2 feature.
3. **Seasonality:** Doesn't account for seasonal trends yet. Rules use 30-day averages only.
4. **Attribution:** Uses last-click attribution (Google Ads default). Doesn't model multi-touch scenarios.
5. **Negative keywords:** Doesn't recommend negative keywords yet (Phase 2 feature).
6. **Audiences:** Doesn't optimize audience targeting, only bid/budget/keywords.

---

## Testing Plan

**Unit Tests:**
- Analysis rules (do they trigger correctly?)
- Proposal generation (is output well-formed?)
- Bid calculation logic (respects min/max bounds?)

**Integration Tests:**
- OAuth token refresh (credentials work?)
- API calls (can fetch real data?)
- Data persistence (can write to DB?)

**Sandbox Tests:**
- Dry run with real API (no actual changes)
- Verify proposals make sense
- Compare against manual audit

**Production Tests:**
- Phase 1 → 2 weeks of read-only data validation
- Phase 2 → Manual approval for all changes (4 weeks)
- Phase 3 → Autonomous execution with guardrails (8 weeks)

---

## Future Enhancements

- [ ] Cross-campaign budget optimization
- [ ] Seasonal adjustment factors
- [ ] Negative keyword discovery
- [ ] Audience expansion recommendations
- [ ] Multi-touch attribution
- [ ] ML-based bid optimization (vs rule-based)
- [ ] Competitor analysis integration
- [ ] Real-time intraday adjustments
