# Long-Term Memory

## Projects

### Orchestrator Agent Platform (Started 2026-02-23)

**Goal:** Multi-client orchestration layer that spawns specialized task agents

**Active Agents:**
1. **Google Ads Manager** — Analyze & optimize multi-client campaigns (phased: read-only → proposals → active mgmt)
2. **Crypto Trading Bot** — Autonomous trading with Stochastic RSI + X sentiment signals
3. **Future:** Email marketing, content creation, etc.

**Key Decisions:**
- Batch multiple Google Ads clients per run (cost-efficient)
- Crypto sentiment via X API (Basic tier $200/month)
- Security-first: Encrypted vault (AWS Secrets Manager or Vault), security audit before production
- Phase plan: Credentials → Build → Sandbox → $1K portfolio → Scale

**Credentials to Generate (from scratch):**
- X Developer API (10-15 min)
- Google Ads API (30-45 min)
- Coinbase Pro API (15-20 min)

**Architecture Pending:**
- Compute environment (local, AWS, VPS?)
- Persistence layer (SQLite, PostgreSQL, DynamoDB?)
- Monitoring strategy (CloudWatch, ELK, email alerts?)

**Documentation:** `/home/brad/.openclaw/workspace/projects/orchestrator/`
- `PROJECT_SUMMARY.md` — Executive summary & next steps
- `requirements.md` — Full spec (all 5 points)
- `SECURITY_REVIEW.md` — 10-point audit checklist
- `CREDENTIALS_SETUP.md` — Step-by-step credential generation

**Status:** Requirements complete → Awaiting deployment infrastructure decision (Point 5)

---

## About Brad

- **Timezone:** America/Los_Angeles
- **Vibe:** Builder/entrepreneur, automation-focused, wants to delegate via agents
- **Preference:** Start cautious, build confidence, then scale
- **Careful:** Wants thorough security review before crypto trading goes live ✓

---

## Hardware & Local LLM Setup (Started 2026-03-02)

**Initial decision:** GTX 1650 4GB for local LLM inference on HP 8000 compact desktop
- Considered RTX 3050 6GB but PSU constraints (HP 8000 ~300W) made it risky
- Chose GTX 1650 (25W, no extra connectors needed)
- **Goal:** Privacy + cost savings (no token bills)

**Status Update (2026-03-02 23:06):** GTX 1650 incompatible with HP 8000 firmware
- Hardware/firmware mismatch (cause TBD: BIOS, PCIe, drivers, or other)
- **Decision:** Abandon local LLM path on HP 8000 for now
- Revisit when different hardware available or compatibility improves
