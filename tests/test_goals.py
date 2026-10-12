def test_get_goals(client):
    """Test retrieving user fitness goals."""
    response = client.get('/api/goals')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'daily_step_goal' in data['data']
    assert 'weekly_workout_goal' in data['data']
    assert 'daily_water_goal' in data['data']

def test_update_goals_success(client):
    """Test updating user fitness goals."""
    payload = {
        "daily_step_goal": 10000,
        "weekly_workout_goal": 6,
        "daily_water_goal": 3.0
    }
    response = client.put('/api/goals', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['daily_step_goal'] == 10000
    assert data['data']['weekly_workout_goal'] == 6
    assert data['data']['daily_water_goal'] == 3.0

def test_update_goals_invalid_data(client):
    """Test updating goals with invalid non-positive numbers."""
    payload = {
        "daily_step_goal": -100,
        "daily_water_goal": 0
    }
    response = client.put('/api/goals', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'errors' in data
