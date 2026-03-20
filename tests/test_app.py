import pytest
from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test home route returns 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_health_route(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_health_returns_json(client):
    """Test health endpoint returns valid JSON"""
    response = client.get('/health')
    assert response.content_type == 'application/json'
