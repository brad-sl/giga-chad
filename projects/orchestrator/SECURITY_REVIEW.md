# Security Review Checklist

**Before going live with crypto trading, this security audit must pass.**

**Status:** Pre-build (to be completed before Phase 1 production)
**Date Started:** 2026-02-23

---

## 1. Credential Management ✓ Required

- [ ] All credentials stored in encrypted vault (AWS Secrets Manager / HashiCorp Vault / OpenClaw native)
- [ ] No hardcoded secrets in code, config files, or git history
- [ ] `.env` files added to `.gitignore` with comprehensive coverage
- [ ] Credential rotation strategy documented & automated where possible
- [ ] Access control: Each agent gets minimum-privilege API scopes
- [ ] Audit logging: Track who accessed which credentials, when
- [ ] Credential generation SOP documented (for Brad to execute)

## 2. API Key Scope & Permissions ✓ Required

### Google Ads API
- [ ] Service account created (not personal account)
- [ ] Scopes limited to required operations only (no delete/archive permissions for MVP)
- [ ] IP whitelist applied (if supported)
- [ ] Test account used first before production client accounts

### Coinbase Pro API
- [ ] Trading API key (not withdrawal key)
- [ ] IP whitelist applied (restrict to deployment servers)
- [ ] Rate limits understood and enforced in code
- [ ] Fallback auth method documented (manual approval for large trades?)
- [ ] Sandbox testing before production deployment

### X Developer API
- [ ] OAuth 1.0a credentials securely stored
- [ ] Rate limits: 10K posts/month monitored (alerts if approaching limit)
- [ ] No sensitive tweet data logged
- [ ] Terms of Service compliance checked (no undisclosed trading)

## 3. Code & Deployment Security ✓ Required

- [ ] Code review by second party (not just Brad)
- [ ] No debug logging of sensitive data (tokens, API responses with secrets)
- [ ] Secrets manager SDK used correctly (no fallback to env vars in prod)
- [ ] Exception handling: Errors don't expose credentials in stack traces
- [ ] Dependencies audited for vulnerabilities (`pip audit`, `safety check`)
- [ ] No eval() or exec() on user input or external data
- [ ] Input validation on all external data (X posts, API responses)

## 4. Agent Isolation & Access Control ✓ Required

- [ ] Each agent runs with its own credentials (no credential sharing)
- [ ] Agent-to-agent communication encrypted (if applicable)
- [ ] Session isolation: agents can't read each other's state/logs
- [ ] OpenClaw sub-agent permissions reviewed (what can each agent do?)
- [ ] Orchestrator validates agent requests before approval

## 5. Financial Controls ✓ Required

- [ ] Position sizing limits enforced in code (max % of portfolio per trade)
- [ ] Daily loss limit / kill-switch if P&L drops below threshold
- [ ] Manual approval gate for first N trades before full automation
- [ ] Trade logging: All trades recorded with timestamp, logic, sentiment score
- [ ] Revert/rollback plan if bot misbehaves (manual Coinbase override)
- [ ] Dry-run mode (paper trading) tested thoroughly before live

## 6. Monitoring & Alerting ✓ Required

- [ ] Real-time dashboard: Bot status, open positions, recent trades
- [ ] Alert thresholds: Unusual activity, API failures, high losses
- [ ] Email/SMS alerts to Brad for critical events
- [ ] Centralized logging (CloudWatch, ELK, Datadog, etc.)
- [ ] Logs retained for 90+ days for audit
- [ ] Error rate monitoring (if >5% of trades fail, auto-pause)

## 7. Incident Response ✓ Required

- [ ] Runbook: What to do if bot trades incorrectly / loses money unexpectedly
- [ ] Pause/kill-switch: Can Brad stop the bot in <1 minute?
- [ ] Forensics: Can we reconstruct what the bot did (logs, trade history)?
- [ ] Liability: What's the max loss tolerance? Should we insure?
- [ ] Incident report template (what to document after an issue)

## 8. Infrastructure Security ✓ Required

- [ ] Deployment environment hardened (AWS/VPS security groups, firewall)
- [ ] SSH/remote access: Key-based auth only, no passwords
- [ ] Automated backups: State/logs backed up off-system
- [ ] Disaster recovery: Can we restore after data loss?
- [ ] Network segmentation: Bot isolated from other systems
- [ ] DDoS / rate-limit protection on APIs

## 9. Compliance & Legal ✓ Required (Informational)

- [ ] X Terms compliance: No undisclosed automated trading
- [ ] Coinbase Pro ToS: Automated trading permitted (check)
- [ ] Regulatory: Is crypto bot trading subject to SEC/FINRA rules?
  - _Note: For personal $10K portfolio likely exempt, but verify_
- [ ] Tax reporting: Bot trades must be logged for tax purposes

## 10. Testing & Validation ✓ Required

- [ ] Unit tests for all trading logic (signals, risk calc, sentiment filter)
- [ ] Integration tests: End-to-end with Coinbase sandbox
- [ ] Backtesting: Historical data sim on 2024-2025 (compare sentiment vs. non-sentiment)
- [ ] Load testing: Can orchestrator handle 10+ agents spawning?
- [ ] Failure mode testing: What happens if X API is down? Coinbase API returns 500?
- [ ] Security testing: Penetration test API integrations if applicable

---

## Execution Plan

1. **Phase 0 (Now):** Generate all credentials, set up vault, document SOPs
2. **Phase 1 (Pre-build):** Security review of architecture + code patterns
3. **Phase 2 (Build):** Implement orchestrator + agents with security controls
4. **Phase 3 (Pre-launch):** Full security audit + penetration test
5. **Phase 4 (Sandbox):** Paper trading for 2+ weeks, monitor 24/7
6. **Phase 5 (Go Live):** Start with $1K portfolio, scale to $10K over 1 month

---

## Sign-Off

- [ ] Brad reviews & approves this checklist
- [ ] All items checked before Phase 1 production
- [ ] Security review documented in project

**Target Date for Security Approval:** TBD
