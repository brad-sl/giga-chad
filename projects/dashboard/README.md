# Dashboard Backend - AI Orchestration Platform

Flask-based REST API for monitoring and managing AI orchestration runs, proposals, and executions.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Server starts on `http://localhost:5000`

## API Endpoints

### Runs
- GET `/api/runs` - List all runs
- POST `/api/runs` - Create new run
- GET `/api/runs/{id}` - Get run details

### Proposals
- GET `/api/proposals` - List proposals
- POST `/api/proposals/{id}/approve` - Approve proposal
- POST `/api/proposals/{id}/reject` - Reject proposal

### Metrics
- GET `/api/metrics/overview` - System metrics

### Health
- GET `/health` - Health check
- GET `/api/status` - Status with DB check

## Database

SQLite database (`orchestrator.db`) with 4 tables:
- runs
- proposals
- executions
- audit_logs

Auto-created on startup.

## Testing

```bash
# Create a run
curl -X POST http://localhost:5000/api/runs \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "test-agent", "agent_type": "test", "status": "completed"}'

# List runs
curl http://localhost:5000/api/runs

# Get metrics
curl http://localhost:5000/api/metrics/overview
```

## Models

- **Run**: Agent execution record
- **Proposal**: Proposed action from agent (pending approval)
- **Execution**: Result of executing approved proposal
- **AuditLog**: Complete audit trail
