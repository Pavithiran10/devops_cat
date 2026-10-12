def test_dashboard_summary_calculation(client):
    """Test dashboard summary endpoint calculations."""
    response = client.get('/api/dashboard')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    today_data = data['data']['today']
    assert 'steps' in today_data
    assert 'distance_km' in today_data
    assert 'calories' in today_data
    assert 'workout_duration_minutes' in today_data
    assert 'water_intake_liters' in today_data
    assert 'step_goal_pct' in today_data
    assert 'weekly_workout_count' in today_data

    # Weekly chart
    weekly_chart = data['data']['weekly_chart']
    assert len(weekly_chart['labels']) == 7
    assert len(weekly_chart['steps']) == 7
    assert len(weekly_chart['calories']) == 7

    # Recent workouts
    assert 'recent_workouts' in data['data']
    assert isinstance(data['data']['recent_workouts'], list)

def test_analytics_metrics_calculation(client):
    """Test analytics endpoint calculations."""
    response = client.get('/api/analytics')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'total_workouts' in data['data']
    assert 'avg_duration_minutes' in data['data']
    assert 'distribution' in data['data']
    assert 'distribution_chart' in data['data']
    assert 'completion_rates' in data['data']

def test_reset_demo_data_endpoint(client):
    """Test the POST /api/reset endpoint."""
    response = client.post('/api/reset')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'reset successfully' in data['message']
