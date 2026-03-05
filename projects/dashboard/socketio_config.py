"""
Flask-SocketIO configuration for real-time dashboard updates.
Handles WebSocket connection setup, event registration, and lifecycle management.
"""

from flask_socketio import SocketIO, emit, join_room, leave_room
import logging

logger = logging.getLogger(__name__)


def init_socketio(app):
    """
    Initialize Flask-SocketIO with the Flask app.
    
    Args:
        app: Flask application instance
    
    Returns:
        SocketIO instance
    """
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",  # In production, restrict this to your domain
        async_mode="threading",
        ping_timeout=10,
        ping_interval=5,
        logger=True,
        engineio_logger=True,
    )
    
    # Register connection handlers
    register_handlers(socketio)
    
    return socketio


def register_handlers(socketio):
    """
    Register WebSocket event handlers.
    
    Args:
        socketio: SocketIO instance
    """
    
    @socketio.on("connect")
    def handle_connect():
        """Handle client connection."""
        logger.info(f"Client connected: {request.sid}")
        emit("connection_response", {
            "status": "connected",
            "message": "Connected to dashboard WebSocket",
            "timestamp": time.time()
        })
    
    @socketio.on("disconnect")
    def handle_disconnect():
        """Handle client disconnection."""
        logger.info(f"Client disconnected: {request.sid}")
    
    @socketio.on("subscribe")
    def handle_subscribe(data):
        """
        Subscribe to a specific run's events.
        
        Args:
            data: {"run_id": "uuid"}
        """
        run_id = data.get("run_id")
        if run_id:
            join_room(f"run_{run_id}")
            logger.info(f"Client {request.sid} subscribed to run {run_id}")
            emit("subscription_response", {
                "status": "subscribed",
                "run_id": run_id,
                "timestamp": time.time()
            })
    
    @socketio.on("unsubscribe")
    def handle_unsubscribe(data):
        """
        Unsubscribe from a specific run's events.
        
        Args:
            data: {"run_id": "uuid"}
        """
        run_id = data.get("run_id")
        if run_id:
            leave_room(f"run_{run_id}")
            logger.info(f"Client {request.sid} unsubscribed from run {run_id}")
            emit("unsubscription_response", {
                "status": "unsubscribed",
                "run_id": run_id,
                "timestamp": time.time()
            })
    
    @socketio.on("heartbeat")
    def handle_heartbeat():
        """Handle client heartbeat/ping."""
        emit("heartbeat_response", {
            "status": "alive",
            "timestamp": time.time()
        })


def emit_event(socketio, event_type, run_id, data):
    """
    Emit a WebSocket event to subscribed clients.
    
    Args:
        socketio: SocketIO instance
        event_type: Type of event ("run_status", "proposal", "log", "execution")
        run_id: The run ID to emit to (clients subscribed to this run)
        data: Event payload
    """
    room = f"run_{run_id}"
    
    event_payload = {
        "type": event_type,
        "run_id": run_id,
        "data": data,
        "timestamp": time.time()
    }
    
    socketio.emit("event", event_payload, room=room)
    logger.debug(f"Emitted {event_type} event to room {room}: {data}")


# Import time and request at module level for handlers
import time
from flask import request
