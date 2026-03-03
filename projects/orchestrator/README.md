# Orchestration Layer Agent

## Overview

Multi-client agent orchestration platform. Central coordinator spawns and manages specialized sub-agents for:
- Google Ads campaign management (multi-client)
- Crypto trading platform
- Other productivity tasks (future)

**Status:** Design phase
**Started:** 2026-02-23

## Architecture Goals

- **Orchestrator:** Central hub. Spawns agents, monitors execution, handles inter-agent communication, aggregates results
- **Task Agents:** Specialized, focused agents spawned on-demand
- **State Tracking:** Persistent tracking of agent runs, outputs, failures
- **Error Handling:** Graceful degradation, retry logic, status reporting

## Requirements

### Point 1: Orchestration Agent ✅
- Spawn subagents via `sessions_spawn`
- Monitor execution via `subagents()`
- Handle errors and retries
- Track state (runs, outputs, failures)
- Inter-agent communication support
- Aggregate and deliver results

### Point 2: Google Ads Agent
_(pending)_

### Point 3: Crypto Trading Platform
_(pending)_

### Point 4: Data/Auth
_(pending)_

### Point 5: Deployment
_(pending)_

## Files

- `design.md` — Architecture + flow diagrams
- `config.example.json` — Config template
- `state-schema.json` — State tracking schema
- `agents/` — Agent implementations (as added)

---

**Next:** Capture remaining requirements (2-5).
