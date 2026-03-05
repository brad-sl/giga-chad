"""Database initialization and schema management."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.create_all()
        print("✅ Database schema initialized")

def reset_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database reset and re-initialized")

def seed_sample_data(app):
    from models import Run, Proposal, Execution, AuditLog
    with app.app_context():
        Run.query.delete()
        Proposal.query.delete()
        Execution.query.delete()
        AuditLog.query.delete()
        run = Run(
            agent_name="google-ads-agent",
            agent_type="google_ads",
            status="completed",
            result={
                "campaigns_analyzed": 3,
                "optimization_suggestions": 5,
                "estimated_roi_improvement": "12.5%"
            },
            error=None,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )
        db.session.add(run)
        db.session.flush()
        proposal = Proposal(
            run_id=run.id,
            agent_name="google-ads-agent",
            proposal_type="campaign_adjustment",
            title="Increase Budget for High-Performing Campaign",
            description="Campaign 'Summer Sale 2024' is showing 15% higher ROI. Recommend increasing daily budget by $50.",
            proposed_data={
                "campaign_id": "12345",
                "campaign_name": "Summer Sale 2024",
                "current_budget": 100,
                "proposed_budget": 150,
                "expected_impact": "+15% ROI"
            },
            approval_status="pending"
        )
        db.session.add(proposal)
        db.session.commit()
        audit = AuditLog(
            run_id=run.id,
            action="run_completed",
            agent_name="google-ads-agent",
            details={
                "campaigns_processed": 3,
                "proposals_generated": 1,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        db.session.add(audit)
        db.session.commit()
        print("✅ Sample data seeded")
