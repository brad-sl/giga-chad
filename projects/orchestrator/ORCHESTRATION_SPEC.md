# Orchestration Spec — Multi-Agent Platform

## Overview

A parent orchestrator that spawns, manages, and coordinates specialized sub-agents for automated business tasks. Agents operate with dedicated responsibilities, shared context, and clear handoff protocols.

**Initial scope:** Google Ads Manager + Crypto Trading Bot  
**Extensible to:** Email marketing, content creation, market analysis, etc.

---

## Architecture

### Parent Orchestrator (Main Session)

**Role:** Spawn agents, monitor health, coordinate communication, aggregate results

**Responsibilities:**
- Spawn sub-agents based on schedule or trigger
- Maintain agent registry (status, uptime, last run)
- Aggregate results from all agents
- Handle inter-agent communication
- Log all activity
- Alert on failures

**Deployment:** Local machine or lightweight VPS (minimal compute, acts as coordinator)

### Sub-Agents (Independent Sessions)

**Role:** Domain-specific autonomous work

**Structure:**
- Google Ads Agent → Fetch data, analyze, propose optimizations, execute on approval
- Crypto Trading Agent → Monitor sentiment, calculate signals, execute trades with guards
- (Future) Email Agent, Content Agent, etc.

**Isolation:** Each agent runs in its own spawned session (`sessions_spawn` with `runtime="subagent"`)

---

## Communication & Data Flow

### Agent Spawn Pattern

```
Parent: sessions_spawn(
  task="Analyze Google Ads campaigns for client X",
  runtime="subagent",
  label="google-ads-manager",
  mode="session"  # persistent, not one-shot
)

Sub-agent receives:
  - Task description
  - Credentials (via secrets manager)
  - Client/portfolio config
  - Prior state (if any)

Sub-agent returns:
  - Structured results (JSON)
  - Logs (for audit trail)
  - Error status (if any)
```

### Inter-Agent Communication

**Parent to Sub-agent:**
- `sessions_send(sessionKey, message)` → Instructions, parameter updates

**Sub-agent to Parent:**
- Return structured output (results, errors, logs)
- Use `sessions_history(sessionKey)` for parent to poll results

### State Persistence

**What's persisted:**
- Agent execution logs (SQLite: timestamp, agent, action, result, error)
- Campaign snapshots (Google Ads: before/after metrics)
- Trade history (Crypto: entry, exit, P&L, sentiment at time)
- Credentials (encrypted vault, not in code)

**Storage:**
- **SQLite** for local development/small scale
- **PostgreSQL** for production multi-client
- **S3** for backups and audit trail

---

## Secrets Management

### Credential Vault

**Requirements:**
- No credentials in code or environment variables (vulnerable)
- Encrypt at rest + in transit
- Rotate keys safely
- Audit who accessed what and when

**Recommended:** AWS Secrets Manager (managed, integrates with Lambda)  
**Alternative:** HashiCorp Vault (self-hosted, more control)

### Credentials Needed

| Agent | API | Credential Type | Scope |
|-------|-----|-----------------|-------|
| Google Ads | Google Ads API | OAuth2 + Refresh Token | Read/Write campaigns, budgets, ads |
| Crypto | Coinbase Pro | API Key + Secret | Trade execution, account balance, orders |
| Sentiment | X (Twitter) | Bearer Token | Read tweets, search (Basic tier $200/mo) |

**Setup:**
1. Generate all credentials from scratch (never reuse personal API keys)
2. Store in vault with descriptive names
3. Grant agents read-only access to relevant secrets
4. Log every access

---

## Deployment Model

### Phase 1: Local Development (Current)

**Where:** Your machine  
**Compute:** Minimal (orchestrator is lightweight)  
**Cost:** Free (your GPU/CPU)  
**Use case:** Testing, learning, validation

**Setup:**
- Parent orchestrator: Python + OpenClaw subagent SDK
- Sub-agents: Spawn as needed
- Storage: SQLite on disk
- Secrets: Encrypted file or Vault instance

### Phase 2: Sandbox VPS

**Where:** Small cloud VM ($5-20/mo, DigitalOcean/Linode)  
**Compute:** 1-2 CPU, 2GB RAM (plenty for lightweight agents)  
**Cost:** $5-20/month + API usage  
**Use case:** 24/7 monitoring, testing at scale, before production

**Setup:**
- Orchestrator runs on VPS (always on)
- Sub-agents spawn on same VPS
- PostgreSQL for persistence
- Vault or AWS Secrets Manager for credentials
- Cron jobs for scheduled runs (Google Ads daily, Crypto every 5 min sentiment check)

### Phase 3: Production Scale

**Where:** AWS Lambda + DynamoDB / or self-hosted Kubernetes  
**Compute:** Auto-scaling (pay per execution)  
**Cost:** $20-200/month (depends on agent frequency)  
**Use case:** Multi-client, high volume, 24/7/365

**Setup:**
- Orchestrator: Lambda (triggered by EventBridge)
- Sub-agents: Lambda or ECS tasks
- DynamoDB for state
- CloudWatch for monitoring
- SNS/SQS for async communication

---

## Monitoring & Alerting

### Metrics to Track

**Per agent:**
- Last run time
- Success/failure rate
- Average execution time
- Errors (with stacktraces)
- Data freshness (when was data last updated?)

**System-level:**
- Total agents running
- Failed spawns
- API quota usage (critical for Google Ads, X API)
- Vault access logs

### Alerting Channels

| Event | Severity | Alert To |
|-------|----------|----------|
| Agent spawn fails | High | Email + Slack |
| API quota exceeded | High | Email (immediate action) |
| Trade execution failed | Critical | Email + SMS |
| Agent hasn't run in 24h | Medium | Slack |
| Vault access anomaly | High | Email + logs |

**Recommended tool:** CloudWatch (AWS) or ELK (self-hosted)

---

## Phased Rollout

### Phase 1A: Infrastructure (This week)

- [ ] Set up Vault/Secrets Manager
- [ ] Create SQLite schema (agents, runs, logs, trades)
- [ ] Build parent orchestrator skeleton
- [ ] Test `sessions_spawn` + `sessions_send` flow

### Phase 1B: Google Ads Agent (Read-Only)

- [ ] Generate Google Ads API credentials
- [ ] Implement agent: fetch accounts → fetch campaigns → fetch performance data
- [ ] Spawn agent, confirm it runs
- [ ] Store results in SQLite
- [ ] Manual review of output

### Phase 1C: Crypto Agent (Dry Run)

- [ ] Generate Coinbase Pro API credentials (read-only first)
- [ ] Fetch X API for sentiment (read-only)
- [ ] Implement agent: monitor sentiment → calculate Stochastic RSI
- [ ] Dry run: log what _would_ trade, don't actually trade
- [ ] Validate signals against historical data

### Phase 2A: Approval Gates

- [ ] Google Ads: Add proposal generation (what changes should we make?)
- [ ] Manual review before execution
- [ ] Crypto: Same—log trades, require human approval first

### Phase 2B: Limited Live Trading

- [ ] Crypto: Start with $1K paper trading (or 0.1 BTC on testnet)
- [ ] Run for 2 weeks, track P&L
- [ ] Validate signal quality, fix any bugs
- [ ] Document learnings

### Phase 3: Full Autonomy

- [ ] Google Ads: Auto-execute approved changes (with guard rails)
- [ ] Crypto: Full autonomous trading (with position limits, stop losses, etc.)
- [ ] Scale to production environment

---

## Error Handling & Guards

### Google Ads Agent

**Guards:**
- Daily spend cap (don't exceed X% of budget in one day)
- Pause campaigns before making changes (avoid mid-flight edits)
- Log all changes + rollback capability
- Require approval before touching high-spend campaigns

**Errors:**
- API rate limit → Backoff + retry
- Invalid credentials → Alert + pause agent
- Campaign not found → Log + skip (may have been deleted)

### Crypto Trading Agent

**Guards:**
- Max position size (never hold >X% of portfolio in one asset)
- Max leverage (no margin trading)
- Stop loss on every trade (auto-exit at X% loss)
- Circuit breaker: if 3 trades lose in a row, pause until manual review
- Slippage protection (don't execute if price moved >Y% since signal)

**Errors:**
- Exchange API down → Backoff + retry, don't re-signal
- Insufficient balance → Alert + pause
- Order rejection → Log reason + adjust params

---

## Testing Strategy

### Unit Tests
- Each agent's core logic (signal calc, optimization logic)
- Mocks for APIs (don't call real APIs in tests)

### Integration Tests
- Spawn agent → feed test data → verify output
- Secrets retrieval works
- Database writes work

### Sandbox Tests
- Real API credentials (read-only)
- Real data flow, no actual execution
- 48-hour dry run before live trading

### Monitoring Tests
- Alerts fire correctly
- Logging captures all relevant info
- Metrics are accurate

---

## Security Checklist

- [ ] All credentials encrypted at rest + in transit
- [ ] Agents run with minimal IAM permissions (least privilege)
- [ ] Audit log for every API call + data access
- [ ] No secrets in logs
- [ ] Rate limiting on agent spawns (prevent abuse)
- [ ] Code reviewed before live trading
- [ ] Rollback plan for each agent (how to undo?)
- [ ] Regular security audit (quarterly)

---

## Success Criteria

**Phase 1 (Read-only):**
- ✅ Google Ads agent fetches data reliably
- ✅ Crypto agent monitors sentiment without errors
- ✅ Data logged cleanly

**Phase 2 (Proposals):**
- ✅ Agents generate actionable proposals
- ✅ Manual review catches bad recommendations
- ✅ Execution works when approved

**Phase 3 (Autonomous):**
- ✅ Google Ads agent autonomously optimizes with measurable ROI gain
- ✅ Crypto agent trades profitably (net positive after fees)
- ✅ System runs 24/7 without manual intervention
- ✅ Audit trail shows clean operation history

---

## Timeline Estimate

| Phase | Effort | Calendar |
|-------|--------|----------|
| Phase 1A (Infra) | 8-12h | 2-3 days |
| Phase 1B (Ads Read) | 12-16h | 3-4 days |
| Phase 1C (Crypto Dry) | 12-16h | 3-4 days |
| Phase 2A+B (Approval + Limited) | 16-24h | 1 week |
| Phase 3 (Production) | 8-12h | 2-3 days |
| **Total** | **56-80h** | **~4-5 weeks** |

---

## Next Steps

1. **Review & approve** this orchestration spec
2. **Choose secrets manager** (AWS Secrets Manager or Vault?)
3. **Choose deployment environment** (local, VPS, or AWS from start?)
4. **Create detailed feature specs** for each agent (see separate docs)
5. **Start Phase 1A** (infrastructure setup)
