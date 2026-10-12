from datetime import date

def test_get_activity_list(client):
    """Test retrieving list of daily activities."""
    response = client.get('/api/activity')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0

def test_get_activity_by_date(client):
    """Test retrieving activity for today's date."""
    today_str = date.today().isoformat()
    response = client.get(f'/api/activity?date={today_str}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data'] is not None
    assert data['data']['activity_date'] == today_str

def test_create_activity_success(client):
    """Test creating an activity record for a new date."""
    target_date = "2026-01-01"
    payload = {
        "activity_date": target_date,
        "steps": 10500,
        "calories": 2600,
        "distance": 7.8,
        "water_intake": 3.0,
        "active_minutes": 75
    }
    response = client.post('/api/activity', json=payload)
    assert response.status_code in (200, 201)
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['steps'] == 10500
    assert data['data']['distance'] == 7.8
    assert data['data']['water_intake'] == 3.0

def test_update_activity_upsert(client):
    """Test updating existing activity record via POST."""
    target_date = date.today().isoformat()
    payload = {
        "activity_date": target_date,
        "steps": 12000,
        "water_intake": 3.5
    }
    response = client.post('/api/activity', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['steps'] == 12000
    assert data['data']['water_intake'] == 3.5

def test_create_activity_invalid_data(client):
    """Test validation errors on negative values."""
    payload = {
        "activity_date": "2026-02-01",
        "steps": -500,
        "water_intake": -2.0
    }
    response = client.post('/api/activity', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'errors' in data
