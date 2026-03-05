"""SQLAlchemy ORM models for the orchestration dashboard."""
from datetime import datetime
from database import db

class Run(db.Model):
    __tablename__ = "runs"
    id = db.Column(db.Integer, primary_key=True)
    agent_name = db.Column(db.String(255), nullable=False)
    agent_type = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    result = db.Column(db.JSON, nullable=True)
    error = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    proposals = db.relationship("Proposal", back_populates="run", cascade="all, delete-orphan")
    executions = db.relationship("Execution", back_populates="run", cascade="all, delete-orphan")
    audit_logs = db.relationship("AuditLog", back_populates="run", cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

class Proposal(db.Model):
    __tablename__ = "proposals"
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    agent_name = db.Column(db.String(255), nullable=False)
    proposal_type = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    proposed_data = db.Column(db.JSON, nullable=False)
    approval_status = db.Column(db.String(50), nullable=False)
    approved_by = db.Column(db.String(255), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    run = db.relationship("Run", back_populates="proposals")
    execution = db.relationship("Execution", back_populates="proposal", uselist=False, cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "run_id": self.run_id,
            "agent_name": self.agent_name,
            "proposal_type": self.proposal_type,
            "title": self.title,
            "description": self.description,
            "proposed_data": self.proposed_data,
            "approval_status": self.approval_status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class Execution(db.Model):
    __tablename__ = "executions"
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    proposal_id = db.Column(db.Integer, db.ForeignKey("proposals.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    result = db.Column(db.JSON, nullable=True)
    error = db.Column(db.Text, nullable=True)
    rollback_data = db.Column(db.JSON, nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    run = db.relationship("Run", back_populates="executions")
    proposal = db.relationship("Proposal", back_populates="execution")
    def to_dict(self):
        return {
            "id": self.id,
            "run_id": self.run_id,
            "proposal_id": self.proposal_id,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "rollback_data": self.rollback_data,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    agent_name = db.Column(db.String(255), nullable=False)
    actor = db.Column(db.String(255), nullable=True)
    details = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    run = db.relationship("Run", back_populates="audit_logs")
    def to_dict(self):
        return {
            "id": self.id,
            "run_id": self.run_id,
            "action": self.action,
            "agent_name": self.agent_name,
            "actor": self.actor,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
