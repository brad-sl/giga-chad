# Crypto Trading Agent — Feature Specification

## Overview

An autonomous agent that trades crypto using technical analysis (Stochastic RSI) + sentiment analysis (X/Twitter signals). Operates with strict risk management, position limits, and human-approved entry points during sandbox phase.

**Primary Goal:** Consistent profitable trading with >2:1 risk/reward ratio and <10% monthly drawdown.

**Target Assets:** BTC, ETH (expanding to altcoins in Phase 2)

**Trading Venue:** Coinbase Pro (later: Kraken, Binance as alternatives)

---

## Functional Requirements

### Phase 1: Sentiment Analysis & Signal Generation (Read-Only)

**Input:**
- Asset to monitor (BTC, ETH)
- Time window (last 24h, 7d, 30d)
- Sentiment sources (X API search)
- RSI lookback period (14 periods typical)

**Process:**

**1. Fetch Price & RSI Data**
```
For each asset (BTC, ETH):
  → Get OHLCV (open, high, low, close, volume) for last 30 periods (hourly or 4h candles)
  → Calculate Stochastic RSI:
     • RSI(14) = standard RSI over 14 periods
     • Stochastic = (RSI - min RSI over 14) / (max RSI over 14 - min RSI over 14)
     • %K line = 3-period moving average of Stochastic
     • %D line = 3-period moving average of %K
  → Store for signal generation
```

**2. Fetch X Sentiment Data**
```
Query X API for mentions + sentiment:
  Keywords: "bitcoin", "ethereum", "BTC", "ETH", "#bitcoin", "#crypto"
  Time window: Last 24 hours
  Metrics to extract:
    • Tweet volume (# mentions)
    • Sentiment score (positive/negative/neutral using NLP or X API)
    • Influencer sentiment (tweets from large accounts, weighted)
    • Trend direction (↑ mentions trending up? down?)
```

**3. Generate Signals**

```
Signal Logic:

BUY Signal when:
  (Stochastic RSI < 20)  // Oversold
  AND (Stochastic %K crosses above %D)  // Momentum turning up
  AND (X sentiment positive OR neutral last 24h)  // No bad news

SELL Signal when:
  (Stochastic RSI > 80)  // Overbought
  AND (Stochastic %K crosses below %D)  // Momentum turning down
  AND (X sentiment negative OR bad news)  // Confirmation

NEUTRAL:
  Everything else (no trade)
```

**Output:**

```json
{
  "run_id": "signal-20260303-001",
  "timestamp": "2026-03-03T14:00:00Z",
  "asset": "BTC",
  "price": 68450.00,
  "signal": "BUY",
  "confidence": 0.78,
  "components": {
    "stochastic_rsi": {
      "value": 18.5,
      "k_line": 22.3,
      "d_line": 28.9,
      "status": "oversold + k crosses above d"
    },
    "sentiment": {
      "x_mentions_24h": 45230,
      "sentiment_score": 0.62,
      "sentiment_trend": "improving",
      "influencer_mentions": 280,
      "key_topics": ["bullish", "accumulation", "adoption"]
    }
  },
  "recommendation": {
    "action": "CONSIDER_BUY",
    "suggested_entry": 68200,
    "entry_reason": "Oversold + positive sentiment"
  }
}
```

**Error Handling:**
- X API down → Use price signal only (technical only)
- Crypto exchange data stale → Wait for fresh data, don't trade on old prices
- Sentiment data incomplete → Flag signal as "low confidence", still log it

**Logging:**
- Every signal generated (even NEUTRAL, for backtesting)
- All inputs (price, RSI, sentiment score)
- Decision tree (which conditions triggered/failed)

---

### Phase 2: Order Execution (Sandbox/Approval)

**Input:**
- Approved signal (from Phase 1, manually approved)
- Entry price (from signal)
- Account balance
- Position sizing rules
- Risk parameters

**Process:**

**1. Validate Pre-Trade Conditions**

```
Checks before order:
  ☐ Account has sufficient balance (with 10% cash reserve)
  ☐ Signal is fresh (< 5 minutes old)
  ☐ Current price hasn't moved >5% from signal generation
  ☐ No existing position in this asset (avoid double-entry)
  ☐ Daily trade limit not exceeded (max 5 trades/day)
  ☐ Total position size doesn't exceed 30% of portfolio
```

**2. Calculate Position Size (Risk-Based)**

```
Risk Management Formula:

Account size: $10,000 (example)
Risk per trade: 2% of account = $200
Entry price: $68,450
Stop loss price: $67,000 (entry - 2%)
Loss per unit: $68,450 - $67,000 = $1,450

Position size = Risk amount / Loss per unit
Position size = $200 / $1,450 = 0.138 BTC

Execute: BUY 0.138 BTC at limit $68,450
```

**3. Place Order**

```
API: Coinbase Pro
  POST /orders
  {
    "product_id": "BTC-USD",
    "side": "buy",
    "order_type": "limit",
    "price": 68450.00,
    "size": 0.138,
    "post_only": false,  // execute immediately if possible
    "stop": "loss",
    "stop_price": 67000.00
  }

Response:
  {
    "order_id": "d0c5340b-6d6c-49d9-b567-48c2f67b6552",
    "status": "pending",
    "created_at": "2026-03-03T14:05:22Z"
  }
```

**4. Record Trade**

```json
{
  "trade_id": "trade-20260303-001",
  "asset": "BTC",
  "signal_id": "signal-20260303-001",
  "entry_time": "2026-03-03T14:05:22Z",
  "entry_price": 68450.00,
  "position_size": 0.138,
  "order_id": "d0c5340b-6d6c-49d9-b567-48c2f67b6552",
  "status": "open",
  "stop_loss": 67000.00,
  "take_profit": 70000.00,
  "risk_reward_ratio": 1.5,
  "reason": "Stochastic oversold + positive sentiment"
}
```

**5. Monitor Position**

```
While position is open:
  Every 1 hour:
    ☐ Check if stop loss is hit → AUTO-CLOSE
    ☐ Check if take profit is hit → AUTO-CLOSE
    ☐ Check if new sentiment signal contradicts entry → Consider exit
    ☐ Check if any risk guard triggered → Alert + consider exit

Guard conditions:
  • Max holding time: 7 days (exit regardless of P&L)
  • Portfolio max loss: 5% daily drawdown (pause all trading)
  • Max position size: 30% of portfolio
  • Emergency stop: Price moves >10% against position
```

---

### Phase 3: Full Autonomous Trading

**Entry Requirements:**
- 50+ trades in sandbox with >55% win rate
- Average risk/reward ratio >1.5:1
- No sustained drawdown >10%

**Additional Features for Autonomy:**

1. **Multi-Asset Management**
   - Track up to 5 assets simultaneously (BTC, ETH, SOL, ADA, XRP)
   - Ensure no two assets >30% of portfolio
   - Total exposed capital never >80% of portfolio

2. **Trailing Stop Loss**
   - After trade is +5% profitable, move stop to 2% below current price
   - Lock in gains while maintaining upside

3. **Profit-Taking Tiers**
   - At +3%: Sell 25% of position, move stop to breakeven
   - At +6%: Sell another 25%, move stop to +2%
   - At +10%: Sell another 25%, let remaining 25% run with +5% trailing stop

4. **Exit Signals (Automatic Sell)**
   ```
   Exit if:
     • Stop loss hit (automatic via exchange)
     • Take profit hit (automatic via exchange)
     • Trailing stop hit (automatic via exchange)
     • Sentiment dramatically reverses (negative spike on X)
     • Max holding time (7 days)
     • Portfolio loss exceeds 5% daily
   ```

**Order Types (Phase 3 only):**
- **Limit orders** (default, safer, higher control)
- **Market orders** (only if limit order fails after 2 min, urgent sentiment)
- **Stop orders** (for automatic exits)
- NO margin/leverage trading (too risky for autonomous)

---

## Technical Implementation

### Signal Quality Assurance

**Backtesting:**
```
Before going live, test on historical data:
  • Last 2 years of price data
  • Last 6 months of X sentiment data (if available)
  • Calculate: win rate, avg profit per trade, max drawdown, Sharpe ratio
  
Acceptance criteria:
  • Win rate > 50%
  • Sharpe ratio > 1.0
  • Max drawdown < 10%
  • Avg profit/trade > 1.5 * avg loss/trade (1.5:1 ratio)
```

**Paper Trading (Sandbox):**
```
Run for 2-4 weeks before live:
  • Generate real signals
  • Execute on Coinbase Sandbox environment
  • Track P&L (hypothetical)
  • Validate signal quality
  • Adjust RSI periods/thresholds if needed
```

**Live Trading (Phased):**
```
Phase 3A (Week 1-2): $100 capital
Phase 3B (Week 3-4): $500 capital (if +10% return)
Phase 3C (Week 5-8): $1,000 capital (if +20% return)
Phase 3D (Scaling): Scale up by 50% monthly if +15% return
```

---

## Input/Output Specifications

### Agent Input (Signal Generation)

```json
{
  "task": "Generate trading signals for crypto assets",
  "assets": ["BTC", "ETH"],
  "timeframe": "4h",  // 1h, 4h, 1d
  "rsi_period": 14,
  "lookback_periods": 30,
  "sentiment_enabled": true,
  "sentiment_keywords": ["bitcoin", "ethereum", "crypto"],
  "api_credentials": {
    "coinbase_vault_key": "coinbase-pro-sandbox",
    "x_api_vault_key": "x-api-basic-tier"
  }
}
```

### Agent Output (Signal Generation)

```json
{
  "run_id": "signal-20260303-001",
  "timestamp": "2026-03-03T14:00:00Z",
  "signals": [
    {
      "asset": "BTC",
      "price": 68450.00,
      "signal": "BUY",
      "confidence": 0.78,
      "components": {
        "stochastic_rsi": 18.5,
        "sentiment_score": 0.62,
        "technical_strength": "strong"
      },
      "action": "PROPOSE_TRADE",
      "suggested_entry": 68200,
      "suggested_stop": 67000,
      "suggested_take_profit": 70000
    },
    {
      "asset": "ETH",
      "price": 3820.00,
      "signal": "NEUTRAL",
      "confidence": 0.45,
      "action": "NO_ACTION"
    }
  ]
}
```

### Agent Input (Trade Execution)

```json
{
  "task": "Execute approved trades",
  "trades_to_execute": [
    {
      "signal_id": "signal-20260303-001",
      "asset": "BTC",
      "action": "BUY",
      "entry_price": 68450.00,
      "position_size_percent": 2.0,  // 2% risk
      "stop_loss": 67000.00,
      "take_profit": 70000.00
    }
  ],
  "api_credentials": {
    "coinbase_vault_key": "coinbase-pro-live",
    "sandbox_mode": true  // set to false only for live trading
  }
}
```

### Agent Output (Trade Execution)

```json
{
  "run_id": "exec-20260303-001",
  "timestamp": "2026-03-03T14:05:30Z",
  "trades_executed": [
    {
      "trade_id": "trade-20260303-001",
      "asset": "BTC",
      "order_id": "d0c5340b-6d6c-49d9-b567-48c2f67b6552",
      "status": "filled",
      "entry_price": 68450.00,
      "position_size": 0.138,
      "entry_time": "2026-03-03T14:05:22Z",
      "stop_loss": 67000.00,
      "take_profit": 70000.00
    }
  ],
  "portfolio_snapshot": {
    "total_balance_usd": 9800.00,
    "cash_usd": 9500.00,
    "positions": {
      "BTC": {
        "size": 0.138,
        "entry_price": 68450.00,
        "current_price": 68475.00,
        "unrealized_pnl": 34.35
      }
    }
  }
}
```

---

## Error Handling & Safeguards

### Pre-Trade Guards

| Guard | Trigger | Action |
|-------|---------|--------|
| Insufficient balance | Balance < 110% needed | Reject trade, alert |
| Signal too old | > 5 min | Reject, regenerate signal |
| Price moved too much | >5% since signal | Reject, regenerate signal |
| Daily trade limit | Already 5 trades | Reject, queue for next day |
| Position size too large | Would be >30% portfolio | Reduce size, execute smaller |
| Portfolio loss limit | Daily loss >5% | Pause all trading, alert |

### Mid-Trade Monitoring

| Condition | Action |
|-----------|--------|
| Stop loss hit | AUTO-CLOSE (exchange order) |
| Take profit hit | AUTO-CLOSE (exchange order) |
| Price moves against 10% | Alert + manual review required |
| Exchange API down | Hold position, don't close |
| Balance error detected | Pause trading, investigate |

### Post-Trade Logging

```
Every trade closes → Log:
  • Entry price, exit price, P&L
  • Holding time
  • Why it closed (SL, TP, time limit, sentiment)
  • Percentage return
  • Cumulative month P&L
```

---

## Non-Functional Requirements

### Performance

- **Signal generation:** <30s per asset
- **Order execution:** <2s per trade
- **Monitoring loop:** Run every 1 hour
- **Data freshness:** Real-time price (< 1min), hourly sentiment (< 1h old)

### Reliability

- **Exchange connectivity:** 99.5% uptime (Coinbase API reliability)
- **Retry logic:** 3 attempts per failed API call
- **Fallback:** If exchange down, hold position, don't panic-sell
- **Data consistency:** Every order has a recorded trade entry

### Security

- **API keys:** Vault-only, never in logs/code
- **Orders:** Only on verified account (identity confirmed)
- **Audit trail:** Every trade logged with agent ID + timestamp
- **No leverage:** Cash-only trading (no margin)

### Observability

- **Logging:** Every signal, every order, every error
- **Metrics:** Win rate, avg profit/trade, Sharpe ratio, portfolio balance, P&L
- **Alerts:** Sent to email/Slack on major events (big wins, losses, errors)
- **Dashboard:** Real-time portfolio view, trade history, P&L curve

---

## Risk Parameters

### Portfolio Risk

```
Account size: $10,000
Risk per trade: 2% ($200)
Max position size: 30% of portfolio
Max daily loss: 5% ($500)
Max monthly loss: 15% ($1,500)

If max loss hit:
  → Pause all trading
  → Alert human (email + Slack)
  → Wait for manual review + restart
```

### Individual Trade Risk

```
Risk/Reward ratio: Minimum 1.5:1 (1% risk, 1.5% potential reward)
Holding time: Max 7 days per trade
Stop loss: Always placed (no exceptions)
Take profit: Always placed (target >1.5x risk)
```

### Leverage & Margin

```
NO margin trading
NO leverage
NO short selling (only long)
Cash only (100% of position funded)
```

---

## Testing Plan

**Unit Tests:**
- RSI calculation (vs manual spreadsheet)
- Stochastic calculation (vs technical analysis library)
- Position sizing logic (risk calculations correct?)
- Sentiment scoring (mock X API, verify scores)

**Integration Tests:**
- Fetch real price data (can connect to exchange?)
- Fetch real sentiment (can connect to X API?)
- Order placement on Sandbox (API works?)
- Database logging (trades saved correctly?)

**Paper Trading (2-4 weeks):**
- Real signals, fake execution
- Track P&L (hypothetical)
- Validate signal quality
- Collect stats (win rate, Sharpe, drawdown)

**Live Trading (Phased):**
- Week 1-2: $100 capital (validate everything works)
- Week 3-4: Scale to $500 (if >10% return)
- Week 5-8: Scale to $1,000 (if >20% return)
- Month 2+: Scale by 50% monthly (if >15% return)

---

## Success Metrics

**Phase 1 (Signals):**
- ✅ Generate signals without errors
- ✅ Backtest shows >50% win rate
- ✅ Backtest shows Sharpe >1.0

**Phase 2 (Sandbox):**
- ✅ 50+ paper trades with >55% win rate
- ✅ <10% drawdown
- ✅ Average trade profit > 1.5 * average loss

**Phase 3 (Live):**
- ✅ Profitable after fees (>15% annual return)
- ✅ Consistent (monthly returns within 5% of average)
- ✅ Low drawdown (<10% monthly)
- ✅ Executed 100+ trades without major bugs

---

## Known Limitations & Future Enhancements

**Current Limitations:**
- Single timeframe (4h only) — Phase 2 adds multi-timeframe
- No support for altcoins yet — Phase 2 expands to top 20 by market cap
- No correlation analysis (all assets treated independently) — Phase 2 adds
- Sentiment from X only — Phase 2 adds Telegram, Discord, news feeds
- No machine learning (rule-based only) — Phase 3 could add ML model

**Future Enhancements:**
- [ ] Multi-timeframe analysis (1h, 4h, 1d together)
- [ ] Altcoin support (SOL, ADA, XRP, AVAX)
- [ ] Cross-asset correlation (avoid correlated positions)
- [ ] Advanced sentiment (NLP analysis, not just mentions)
- [ ] ML-based signal optimization
- [ ] DCA (dollar-cost-averaging) for trending markets
- [ ] Options trading (for defined risk)
- [ ] Grid trading (entry at multiple price levels)

---

## Dependencies

- **Exchange API:** Coinbase Pro (read: public quotes, write: orders)
- **Sentiment API:** X API (Twitter) - Basic tier $200/mo
- **Libraries:** `ccxt` (crypto exchange), `pandas` (data), `ta-lib` (technical), `tweepy` (Twitter), `requests`
- **Data:** Historical OHLCV (crypto exchange), Historical sentiment (X API backfill or archive)
- **Secrets:** Coinbase API key + secret, X API bearer token
