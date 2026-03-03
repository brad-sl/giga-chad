# Requirements & Design Decisions

**Captured:** 2026-02-23 20:05 PST

## Point 1: Orchestration Agent ✅

**Role:** Central hub for spawning and managing task-specific agents

**Capabilities:**
- Spawn subagents via `sessions_spawn`
- Monitor execution via `subagents()`
- Handle errors and retries
- Track state (runs, outputs, failures)
- Support inter-agent communication
- Aggregate and deliver results

---

## Point 2: Google Ads Agent

**Phased Rollout Approach:**

### Phase 1: Analysis & Reporting (MVP)
- Month-over-month performance analysis
- Campaign health checks
- Identify improvement opportunities
- Generate reports for existing clients

**Approach:** Read-only. Safe to build/test without impacting live campaigns.

### Phase 2: Analysis for Proposals
- Analyze client landscape for new business opportunities
- Generate campaign proposals for prospects

### Phase 3: Active Management (future)
- Keyword optimization
- Ad copy A/B testing
- Target CPA adjustments
- Conversion tracking setup
- Pause/activate campaigns (cautious, gated?)

**Multi-client handling:**
- **Approach:** Batch multiple clients in a single agent run for cost efficiency
- Each client has separate Google Ads account / API credentials (isolated within batch)
- Plan refactor to per-client spawns as volume/complexity grows
- **Rationale:** Minimize model invocations early; flexibility to scale later

**Reporting:**
- **Format:** Email summaries
- **Schedule:** Weekly (automated)
- **On-demand:** Ad-hoc report requests also supported (manual trigger)
- **Delivery:** Email to Brad (client distribution TBD)

---

## Point 3: Crypto Trading Platform

**Status:** Fully specified with sentiment integration

### Core Architecture

**Trading Engine:**
- Stochastic RSI-based signals (14, 3, 3)
- ATR-based risk management
- Coinbase Pro integration
- Real-time execution
- Backtesting module (historical data simulation)
- Volatility detection

**Target Assets:** Memecoins (SHIB, DOGE, WIF), news-sensitive coins (XRP)

**Technical Stack:**
- Python-based
- Coinbase Pro API
- Offline sentiment analysis (VADER)
- Historical data backtesting

### Sentiment Integration (X / Twitter)

**Purpose:** Confirm/filter StochRSI signals with real-time social sentiment

**API Tier:** Basic ($200/month recommended)
- 10,000 posts/month read limit
- ~300-500 daily fetches possible (30-50 posts per coin, 10 coins)
- Setup time: 10-15 minutes
- OAuth 1.0a authentication required

**Libraries:**
- `tweepy` — X API client
- `vaderSentiment` — Rule-based sentiment analysis (-1 to +1)
- Optional: `textblob` for simpler analysis

**Implementation:**
- Fetch recent X posts (exclude retweets)
- Compute average sentiment score
- Filter trades: Buy only if sentiment > 0.2 (bullish), Sell if < -0.2 (bearish)
- Fallback to neutral (0.0) on API error
- ~10-20 lines of code addition; 1-2 hours total setup

**Rate Limiting:** 1-2 seconds per coin to avoid throttling

### Expected Performance Impact

**Positive:**
- Improved signal accuracy: 60% → 65-70% win rate
- Better risk management in volatile markets
- 5-10% higher annual ROI potential
- Captures sentiment-driven reversals (XRP ETF hype, memecoin pumps)

**Negative:**
- Added API latency (1-2 sec per coin)
- Monthly cost: $200 (Basic tier)
- Bot noise distorts sentiment (~15% of crypto tweets are bots)
- Over-filtering in bearish periods may reduce trade frequency
- Potential 2-5% ROI loss if sentiment data unreliable

**Cost Analysis:**
- $200/month API = ~2% of $10,000 portfolio annually
- Offset by 5-10% ROI gain = net positive

### Execution Model

**Deployment:**
- Python bot running on AWS EC2 or local machine
- Scheduled task for daily/weekly runs
- Sandbox testing in Coinbase Pro before live
- Error handling for API downtime (fallback to neutral)

**Backtest & Validation:**
- Test historical X sentiment (public datasets) vs. 2024-2025 trades
- Paper trading in Coinbase sandbox
- Monitor logs for sentiment scores & accuracy
- Go live post-validation

### Risk Management & Compliance
- Stochastic RSI (14, 3, 3) overbought/oversold thresholds
- ATR-based position sizing
- Sentiment acts as kill-switch for false signals
- X Terms compliance: No solely-automated trading disclosure
- Monitor bot distortion; adjust thresholds as needed

## Point 4: Data/Auth

**Status:** All credentials to be generated from scratch

### Credential Requirements

**Google Ads API:**
- OAuth 2.0 credentials (service account or user-based)
- Scopes: Campaign management, reporting
- Test environment first (sandbox)

**Coinbase Pro API:**
- API Key + Secret
- Passphrase
- Restrict to trading account (not withdrawal)
- IP whitelist recommended

**X Developer API:**
- Consumer Key / Secret
- Access Token / Token Secret
- OAuth 1.0a authentication
- Basic tier subscription ($200/month)
- Setup time: 10-15 minutes

### Credential Storage Strategy

**Requirements:**
- Maximum security for crypto keys
- Easy rotation/updates
- No hardcoded secrets in code/repo
- Audit trail preferred
- Local and remote (AWS) deployment support

**Recommended Approach:**
1. **Primary:** Encrypted vault (e.g., HashiCorp Vault or AWS Secrets Manager)
   - Centralized secret management
   - Audit logging
   - Automatic rotation capability
   - Access control per agent

2. **Development/Testing:** `.env` file + `python-dotenv`
   - Local development only
   - STRICT `.gitignore` (never commit)
   - Not for production

3. **OpenClaw Integration:** Leverage OpenClaw's credential management if available
   - Native support for multi-agent credential isolation
   - Built-in encryption
   - Session-level access control

**Implementation Plan:**
- Use AWS Secrets Manager for production (if AWS deployment)
- Use Vault for self-hosted (if on-prem)
- `.env` + dotenv for local dev with strict gitignore
- Document credential generation steps for each service

---

## Point 5: Deployment ✅

**Status:** Finalized for Google Ads MVP

### Infrastructure

**Compute:** Local OpenClaw instance
- Low resource overhead (lightweight orchestrator only)
- Actual work happens in spawned subagents (on-demand)
- No persistent daemons

**Persistence:** SQLite (local)
- Store reports locally for history
- Simple, no external DB needed

**Scheduling:** Cron job (local) + manual trigger
- Weekly automated reports
- Ad-hoc reports on-demand

**Reporting:**
- Email summaries to Brad
- Local report storage for audit/history
- Format TBD (see Point 2 report design)

### Scaling Plan
- Start: 1 Google Ads client account
- Grow: Add more accounts as workflow stabilizes
- Future: Consider distributed agents if volume requires
