def test_health_check_success(client):
    """Test that the /api/health endpoint returns 200 and healthy status."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get('status') == 'healthy'
    assert data.get('app') == 'FitTrack'
    assert data.get('database') == 'connected'
    assert 'version' in data
    assert 'timestamp' in data
