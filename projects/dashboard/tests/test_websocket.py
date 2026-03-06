import sys
import pytest
import json
sys.path.insert(0, 'projects/dashboard')

from app import create_app
from flask_socketio import SocketIOTestClient

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    socketio = app.socketio
    
    with app.test_client() as c:
        with c.session_transaction() as sess:
            yield socketio.test_client(app)

def test_websocket_connect(client):
    """Test WebSocket connection"""
    assert client.is_connected()

def test_websocket_run_update(client):
    """Test run_status event"""
    client.emit('run_status', {
        'run_id': 'run-1',
        'status': 'running',
        'progress': 50
    })
    
    received = client.get_received()
    assert len(received) > 0

def test_websocket_proposal_event(client):
    """Test proposal_notification event"""
    client.emit('proposal_notification', {
        'proposal_id': 'prop-1',
        'message': 'New proposal awaiting approval'
    })
    
    received = client.get_received()
    assert len(received) > 0

def test_websocket_disconnect(client):
    """Test WebSocket disconnection"""
    client.disconnect()
    assert not client.is_connected()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
