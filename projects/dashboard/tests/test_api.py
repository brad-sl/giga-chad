import sys
import pytest
import json
sys.path.insert(0, 'projects/dashboard')

from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_get_runs(client):
    """Test GET /api/runs"""
    response = client.get('/api/runs')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_run(client):
    """Test POST /api/runs"""
    payload = {
        'agent_id': 'google-ads-manager',
        'phase': 1,
        'status': 'running',
        'clients': ['ABC123']
    }
    response = client.post('/api/runs', json=payload)
    assert response.status_code == 201
    assert response.json['agent_id'] == 'google-ads-manager'

def test_get_proposals(client):
    """Test GET /api/proposals"""
    response = client.get('/api/proposals')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_metrics_overview(client):
    """Test GET /api/metrics/overview"""
    response = client.get('/api/metrics/overview')
    assert response.status_code == 200
    assert 'total_spend' in response.json
    assert 'proposals' in response.json

def test_approve_proposal(client):
    """Test POST /api/proposals/{id}/approve"""
    # Create dummy proposal first
    response = client.post('/api/proposals', json={
        'run_id': 'run-1',
        'client_id': 'ABC123',
        'action_type': 'pause_ad_group',
        'confidence': 'high'
    })
    assert response.status_code == 201
    
    prop_id = response.json['id']
    approve_response = client.post(f'/api/proposals/{prop_id}/approve')
    assert approve_response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
