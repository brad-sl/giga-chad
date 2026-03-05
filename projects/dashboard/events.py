"""
Event emitters for dashboard real-time updates.
Provides functions to emit various event types: run status, proposals, logs, and executions.
"""

from socketio_config import emit_event
import uuid
from datetime import datetime
import json


class DashboardEvents:
    """
    Central event emitter for all dashboard real-time updates.
    """
    
    def __init__(self, socketio):
        """
        Initialize event emitter with SocketIO instance.
        
        Args:
            socketio: Flask-SocketIO instance
        """
        self.socketio = socketio
    
    def emit_run_status_update(self, run_id, status, progress=None, message=None):
        """
        Emit a run status update event.
        
        Event schema:
        {
            "type": "run_status",
            "run_id": "uuid",
            "data": {
                "status": "pending|running|completed|failed",
                "progress": 0-100,
                "message": "Human-readable status message"
            },
            "timestamp": timestamp
        }
        
        Args:
            run_id: Unique identifier for the run
            status: Current status ("pending", "running", "completed", "failed")
            progress: Progress percentage (0-100)
            message: Human-readable status message
        """
        data = {
            "status": status,
        }
        
        if progress is not None:
            data["progress"] = progress
        
        if message is not None:
            data["message"] = message
        
        emit_event(self.socketio, "run_status", run_id, data)
    
    def emit_proposal_notification(self, run_id, proposal_id, title, description, 
                                   changes, impact=None):
        """
        Emit a proposal notification event when a new proposal arrives.
        
        Event schema:
        {
            "type": "proposal",
            "run_id": "uuid",
            "data": {
                "proposal_id": "uuid",
                "title": "Proposal title",
                "description": "Detailed description",
                "changes": [...],
                "impact": "Estimated impact/benefits",
                "requires_approval": true
            },
            "timestamp": timestamp
        }
        
        Args:
            run_id: Associated run ID
            proposal_id: Unique proposal identifier
            title: Proposal title
            description: Detailed description
            changes: List of changes/actions proposed
            impact: Estimated impact (optional)
        """
        data = {
            "proposal_id": proposal_id,
            "title": title,
            "description": description,
            "changes": changes,
            "requires_approval": True
        }
        
        if impact is not None:
            data["impact"] = impact
        
        emit_event(self.socketio, "proposal", run_id, data)
    
    def emit_log_stream(self, run_id, log_level, message, source=None, metadata=None):
        """
        Emit a log stream event for real-time agent output.
        
        Event schema:
        {
            "type": "log",
            "run_id": "uuid",
            "data": {
                "level": "INFO|DEBUG|WARNING|ERROR",
                "message": "Log message",
                "source": "Agent/component name",
                "metadata": {...}
            },
            "timestamp": timestamp
        }
        
        Args:
            run_id: Associated run ID
            log_level: Log level ("INFO", "DEBUG", "WARNING", "ERROR")
            message: Log message
            source: Source of the log (agent name, component, etc.)
            metadata: Additional metadata (optional)
        """
        data = {
            "level": log_level,
            "message": message,
        }
        
        if source is not None:
            data["source"] = source
        
        if metadata is not None:
            data["metadata"] = metadata
        
        emit_event(self.socketio, "log", run_id, data)
    
    def emit_execution_update(self, run_id, execution_id, action, status, 
                             result=None, error=None):
        """
        Emit an execution update event for changes that succeed or fail.
        
        Event schema:
        {
            "type": "execution",
            "run_id": "uuid",
            "data": {
                "execution_id": "uuid",
                "action": "Description of action",
                "status": "success|failed",
                "result": {...},
                "error": "Error message if failed"
            },
            "timestamp": timestamp
        }
        
        Args:
            run_id: Associated run ID
            execution_id: Unique execution identifier
            action: Description of action executed
            status: Execution status ("success" or "failed")
            result: Execution result data (optional)
            error: Error message if execution failed (optional)
        """
        data = {
            "execution_id": execution_id,
            "action": action,
            "status": status,
        }
        
        if result is not None:
            data["result"] = result
        
        if error is not None:
            data["error"] = error
        
        emit_event(self.socketio, "execution", run_id, data)
    
    @staticmethod
    def generate_event_id():
        """Generate a unique event ID."""
        return str(uuid.uuid4())


# Convenience function for creating a DashboardEvents instance
def create_events_handler(socketio):
    """
    Create and return a DashboardEvents instance.
    
    Args:
        socketio: Flask-SocketIO instance
    
    Returns:
        DashboardEvents instance
    """
    return DashboardEvents(socketio)
