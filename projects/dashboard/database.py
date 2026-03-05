"""
Database initialization and schema management for the orchestration dashboard.
"""

import os
import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialize the database with SQLAlchemy app context."""
    with app.app_context():
        db.create_all()
        print("✅ Database schema initialized")


def reset_db(app):
    """Reset the database (drops and recreates all tables)."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database reset and re-initialized")


def seed_sample_data(app):
    """Seed the database with sample data for testing."""
    from models import Run, Proposal, Execution, AuditLog
    
    with app.app_context():
        # Clear existing data
        Run.query.delete()
        Proposal.query.delete()
        Execution.query.delete()
        AuditLog.query.delete()
        
        # Create sample run
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
        db.session.flush()  # Flush to get the run_id
        
        # Create sample proposal
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
        
        # Create audit log
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
