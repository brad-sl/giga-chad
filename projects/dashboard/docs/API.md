# Dashboard API Reference

## Base URL
`http://localhost:5000/api`

## Runs Endpoint

### GET /runs
List all runs.

**Response:**
```json
[
  {
    "run_id": "run-001",
    "agent_id": "google-ads-manager",
    "phase": 1,
    "status": "running",
    "started_at": "2026-03-05T08:00:00Z",
    "completed_at": null,
    "clients_processed": 4,
    "proposal_count": 3
  }
]
```

### POST /runs
Create a new run.

**Request:**
```json
{
  "agent_id": "google-ads-manager",
  "phase": 1,
  "status": "running",
  "clients": ["ABC123", "XYZ789"]
}
```

**Response:** (201)
```json
{
  "run_id": "run-002",
  "agent_id": "google-ads-manager",
  ...
}
```

### GET /runs/{run_id}
Get specific run details.

**Response:**
```json
{
  "run_id": "run-001",
  "agent_id": "google-ads-manager",
  ...
  "campaigns": [...],
  "errors": []
}
```

## Proposals Endpoint

### GET /proposals
List pending proposals.

**Response:**
```json
[
  {
    "proposal_id": "prop-001",
    "run_id": "run-001",
    "action_type": "pause_ad_group",
    "approval_status": "pending",
    "confidence": "high",
    "impact_estimate": {
      "cost_savings": 500,
      "revenue_impact": 0
    }
  }
]
```

### POST /proposals/{id}/approve
Approve a proposal.

**Response:** (200)
```json
{
  "proposal_id": "prop-001",
  "approval_status": "approved",
  "approved_at": "2026-03-05T08:15:00Z"
}
```

### POST /proposals/{id}/reject
Reject a proposal.

**Response:** (200)
```json
{
  "proposal_id": "prop-001",
  "approval_status": "rejected"
}
```

## Metrics Endpoint

### GET /metrics/overview
Get dashboard overview metrics.

**Response:**
```json
{
  "total_spend": 45230.50,
  "proposals_month": 28,
  "approval_rate": 0.82,
  "est_monthly_savings": 3100,
  "changes_executed": 22
}
```

## Error Responses

All endpoints return errors in this format:
```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "status": 400
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad request
- 404: Not found
- 500: Server error
