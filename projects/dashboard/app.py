"""
Flask Dashboard Backend for AI Orchestration Platform

Main application file with REST endpoints for:
- Run management
- Proposal approval/rejection
- Metrics and monitoring
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from database import db, init_db, reset_db, seed_sample_data
from models import Run, Proposal, Execution, AuditLog


# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orchestrator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# ============================================================================
# Database Initialization
# ============================================================================

@app.before_request
def before_request():
    """Ensure database exists before handling request."""
    pass


# ============================================================================
# REST ENDPOINTS: RUNS
# ============================================================================

@app.route('/api/runs', methods=['GET'])
def get_runs():
    """
    GET /api/runs
    Returns a list of all runs with pagination support.
    
    Query params:
      - limit: max number of results (default: 50)
      - offset: pagination offset (default: 0)
      - status: filter by status (pending, running, completed, failed)
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        status_filter = request.args.get('status', None)
        
        query = Run.query
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        total = query.count()
        runs = query.order_by(Run.created_at.desc()).limit(limit).offset(offset).all()
        
        return jsonify({
            'success': True,
            'data': [run.to_dict() for run in runs],
            'total': total,
            'limit': limit,
            'offset': offset,
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/runs', methods=['POST'])
def create_run():
    """
    POST /api/runs
    Create a new run record.
    
    Request body:
      - agent_name (required): Name of the agent
      - agent_type (required): Type of agent (google_ads, crypto, etc.)
      - result (optional): Initial result data
    """
    try:
        data = request.get_json()
        
        if not data or 'agent_name' not in data or 'agent_type' not in data:
            return jsonify({'success': False, 'error': 'agent_name and agent_type required'}), 400
        
        run = Run(
            agent_name=data['agent_name'],
            agent_type=data['agent_type'],
            status=data.get('status', 'pending'),
            result=data.get('result'),
        )
        
        db.session.add(run)
        db.session.commit()
        
        # Log the action
        audit = AuditLog(
            run_id=run.id,
            action='run_created',
            agent_name=run.agent_name,
            details={'run_id': run.id, 'agent_type': run.agent_type}
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': run.to_dict(),
            'message': f'Run {run.id} created'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/runs/<int:run_id>', methods=['GET'])
def get_run(run_id):
    """
    GET /api/runs/{run_id}
    Get detailed information about a specific run including proposals and executions.
    """
    try:
        run = Run.query.get(run_id)
        
        if not run:
            return jsonify({'success': False, 'error': 'Run not found'}), 404
        
        return jsonify({
            'success': True,
            'data': {
                **run.to_dict(),
                'proposals': [p.to_dict() for p in run.proposals],
                'executions': [e.to_dict() for e in run.executions],
                'audit_logs': [a.to_dict() for a in run.audit_logs],
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# REST ENDPOINTS: PROPOSALS
# ============================================================================

@app.route('/api/proposals', methods=['GET'])
def get_proposals():
    """
    GET /api/proposals
    Returns a list of all proposals with pagination and filtering.
    
    Query params:
      - limit: max number of results (default: 50)
      - offset: pagination offset (default: 0)
      - status: filter by approval_status (pending, approved, rejected)
      - agent_name: filter by agent
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        status_filter = request.args.get('status', None)
        agent_filter = request.args.get('agent_name', None)
        
        query = Proposal.query
        
        if status_filter:
            query = query.filter_by(approval_status=status_filter)
        if agent_filter:
            query = query.filter_by(agent_name=agent_filter)
        
        total = query.count()
        proposals = query.order_by(Proposal.created_at.desc()).limit(limit).offset(offset).all()
        
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in proposals],
            'total': total,
            'limit': limit,
            'offset': offset,
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/proposals/<int:proposal_id>/approve', methods=['POST'])
def approve_proposal(proposal_id):
    """
    POST /api/proposals/{id}/approve
    Approve a proposal and optionally execute it.
    
    Request body (optional):
      - approved_by: User who approved
      - auto_execute: Whether to auto-execute (default: false)
    """
    try:
        proposal = Proposal.query.get(proposal_id)
        
        if not proposal:
            return jsonify({'success': False, 'error': 'Proposal not found'}), 404
        
        if proposal.approval_status != 'pending':
            return jsonify({
                'success': False,
                'error': f'Proposal already {proposal.approval_status}'
            }), 400
        
        data = request.get_json() or {}
        
        # Update proposal
        proposal.approval_status = 'approved'
        proposal.approved_by = data.get('approved_by', 'system')
        proposal.approved_at = datetime.utcnow()
        
        db.session.commit()
        
        # Log the action
        audit = AuditLog(
            run_id=proposal.run_id,
            action='proposal_approved',
            agent_name=proposal.agent_name,
            actor=data.get('approved_by', 'system'),
            details={'proposal_id': proposal.id, 'proposal_type': proposal.proposal_type}
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': proposal.to_dict(),
            'message': f'Proposal {proposal_id} approved'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/proposals/<int:proposal_id>/reject', methods=['POST'])
def reject_proposal(proposal_id):
    """
    POST /api/proposals/{id}/reject
    Reject a proposal.
    
    Request body (optional):
      - rejected_by: User who rejected
      - reason: Reason for rejection
    """
    try:
        proposal = Proposal.query.get(proposal_id)
        
        if not proposal:
            return jsonify({'success': False, 'error': 'Proposal not found'}), 404
        
        if proposal.approval_status != 'pending':
            return jsonify({
                'success': False,
                'error': f'Proposal already {proposal.approval_status}'
            }), 400
        
        data = request.get_json() or {}
        
        # Update proposal
        proposal.approval_status = 'rejected'
        proposal.approved_by = data.get('rejected_by', 'system')
        proposal.approved_at = datetime.utcnow()
        
        db.session.commit()
        
        # Log the action
        audit = AuditLog(
            run_id=proposal.run_id,
            action='proposal_rejected',
            agent_name=proposal.agent_name,
            actor=data.get('rejected_by', 'system'),
            details={
                'proposal_id': proposal.id,
                'proposal_type': proposal.proposal_type,
                'reason': data.get('reason', 'No reason provided')
            }
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': proposal.to_dict(),
            'message': f'Proposal {proposal_id} rejected'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# REST ENDPOINTS: METRICS
# ============================================================================

@app.route('/api/metrics/overview', methods=['GET'])
def get_metrics_overview():
    """
    GET /api/metrics/overview
    Returns high-level metrics and statistics about the system.
    """
    try:
        # Count stats
        total_runs = Run.query.count()
        completed_runs = Run.query.filter_by(status='completed').count()
        failed_runs = Run.query.filter_by(status='failed').count()
        
        pending_proposals = Proposal.query.filter_by(approval_status='pending').count()
        approved_proposals = Proposal.query.filter_by(approval_status='approved').count()
        rejected_proposals = Proposal.query.filter_by(approval_status='rejected').count()
        
        # Get recent runs
        recent_runs = Run.query.order_by(Run.completed_at.desc()).limit(5).all()
        
        # Get agents breakdown
        agents = db.session.query(Run.agent_type, db.func.count(Run.id)).group_by(Run.agent_type).all()
        
        return jsonify({
            'success': True,
            'data': {
                'runs': {
                    'total': total_runs,
                    'completed': completed_runs,
                    'failed': failed_runs,
                    'running': Run.query.filter_by(status='running').count(),
                    'pending': Run.query.filter_by(status='pending').count(),
                },
                'proposals': {
                    'pending': pending_proposals,
                    'approved': approved_proposals,
                    'rejected': rejected_proposals,
                    'total': pending_proposals + approved_proposals + rejected_proposals,
                },
                'agents': {agent_type: count for agent_type, count in agents},
                'recent_runs': [r.to_dict() for r in recent_runs],
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# Health Check & Status
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Simple health check endpoint."""
    return jsonify({'status': 'ok'}), 200


@app.route('/api/status', methods=['GET'])
def status():
    """Status endpoint with database connectivity."""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 503


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ============================================================================
# CLI Commands
# ============================================================================

@app.cli.command()
def init():
    """Initialize the database."""
    init_db(app)
    print("✅ Database initialized")


@app.cli.command()
def reset():
    """Reset the database."""
    if input("Are you sure? (yes/no): ").lower() == 'yes':
        reset_db(app)
        print("✅ Database reset")


@app.cli.command()
def seed():
    """Seed sample data."""
    seed_sample_data(app)
    print("✅ Sample data seeded")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    # Create app context and initialize database
    with app.app_context():
        init_db(app)
    
    print("=" * 70)
    print("🚀 Dashboard Backend - Starting on http://localhost:5000")
    print("=" * 70)
    print()
    print("API Endpoints:")
    print("  GET    /api/runs                    - List all runs")
    print("  POST   /api/runs                    - Create a new run")
    print("  GET    /api/runs/{run_id}           - Get run details")
    print("  GET    /api/proposals               - List all proposals")
    print("  POST   /api/proposals/{id}/approve  - Approve a proposal")
    print("  POST   /api/proposals/{id}/reject   - Reject a proposal")
    print("  GET    /api/metrics/overview        - Get metrics overview")
    print()
    print("Management Endpoints:")
    print("  GET    /health                      - Health check")
    print("  GET    /api/status                  - Status with DB check")
    print()
    
    # Run on localhost:5000
    socketio.run(app, host='localhost', port=5000, debug=False)
