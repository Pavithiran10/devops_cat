from datetime import date

def test_get_all_workouts(client):
    """Test retrieving list of all workouts."""
    response = client.get('/api/workouts')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    assert data['count'] > 0

def test_get_workout_by_id_success(client):
    """Test retrieving an existing workout by ID."""
    # List workouts to get an existing ID
    list_res = client.get('/api/workouts')
    workouts = list_res.get_json()['data']
    assert len(workouts) > 0
    workout_id = workouts[0]['id']

    response = client.get(f'/api/workouts/{workout_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['id'] == workout_id
    assert 'workout_type' in data['data']
    assert 'duration' in data['data']

def test_get_workout_by_id_not_found(client):
    """Test retrieving a non-existent workout ID returns 404."""
    response = client.get('/api/workouts/999999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'not found' in data['message'].lower()

def test_create_workout_success(client):
    """Test creating a new workout with valid payload."""
    payload = {
        "workout_type": "Running",
        "duration": 45,
        "calories": 420,
        "distance": 5.2,
        "workout_date": date.today().isoformat(),
        "notes": "Tempo run around park"
    }
    response = client.post('/api/workouts', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['workout_type'] == "Running"
    assert data['data']['duration'] == 45
    assert data['data']['calories'] == 420
    assert data['data']['distance'] == 5.2
    assert data['data']['notes'] == "Tempo run around park"
    assert 'id' in data['data']

def test_create_workout_validation_missing_fields(client):
    """Test workout creation with missing mandatory fields returns 400."""
    # Missing duration and calories
    payload = {
        "workout_type": "Running",
        "workout_date": date.today().isoformat()
    }
    response = client.post('/api/workouts', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'errors' in data

def test_create_workout_validation_invalid_type(client):
    """Test workout creation with invalid workout_type returns 400."""
    payload = {
        "workout_type": "Skydiving",  # Not in allowed list
        "duration": 30,
        "calories": 200,
        "distance": 0,
        "workout_date": date.today().isoformat()
    }
    response = client.post('/api/workouts', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert any("workout_type must be one of" in err for err in data.get('errors', []))

def test_create_workout_validation_negative_numbers(client):
    """Test workout creation with negative duration/calories returns 400."""
    payload = {
        "workout_type": "Walking",
        "duration": -10,
        "calories": -50,
        "distance": -2.0,
        "workout_date": date.today().isoformat()
    }
    response = client.post('/api/workouts', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'

def test_create_workout_validation_invalid_date(client):
    """Test workout creation with malformed date returns 400."""
    payload = {
        "workout_type": "Cycling",
        "duration": 30,
        "calories": 200,
        "workout_date": "invalid-date-string"
    }
    response = client.post('/api/workouts', json=payload)
    assert response.status_code == 400

def test_update_workout_success(client):
    """Test updating an existing workout."""
    # Create workout first
    create_res = client.post('/api/workouts', json={
        "workout_type": "Yoga",
        "duration": 30,
        "calories": 150,
        "distance": 0.0,
        "workout_date": date.today().isoformat(),
        "notes": "Initial notes"
    })
    workout_id = create_res.get_json()['data']['id']

    # Update workout
    update_res = client.put(f'/api/workouts/{workout_id}', json={
        "workout_type": "Yoga",
        "duration": 45,
        "calories": 220,
        "distance": 0.0,
        "workout_date": date.today().isoformat(),
        "notes": "Extended flow session"
    })
    assert update_res.status_code == 200
    data = update_res.get_json()
    assert data['status'] == 'success'
    assert data['data']['duration'] == 45
    assert data['data']['calories'] == 220
    assert data['data']['notes'] == "Extended flow session"

def test_update_workout_not_found(client):
    """Test updating nonexistent workout returns 404."""
    response = client.put('/api/workouts/999999', json={
        "workout_type": "Running",
        "duration": 30,
        "calories": 200,
        "workout_date": date.today().isoformat()
    })
    assert response.status_code == 404

def test_delete_workout_success(client):
    """Test deleting an existing workout."""
    create_res = client.post('/api/workouts', json={
        "workout_type": "Strength Training",
        "duration": 50,
        "calories": 350,
        "distance": 0.0,
        "workout_date": date.today().isoformat()
    })
    workout_id = create_res.get_json()['data']['id']

    delete_res = client.delete(f'/api/workouts/{workout_id}')
    assert delete_res.status_code == 200
    assert 'deleted successfully' in delete_res.get_json()['message']

    # Verify 404 on subsequent get
    verify_res = client.get(f'/api/workouts/{workout_id}')
    assert verify_res.status_code == 404

def test_delete_workout_not_found(client):
    """Test deleting nonexistent workout returns 404."""
    response = client.delete('/api/workouts/999999')
    assert response.status_code == 404

def test_filter_and_sort_workouts(client):
    """Test filtering workouts by type and sorting."""
    res_running = client.get('/api/workouts?type=Running')
    assert res_running.status_code == 200
    for w in res_running.get_json()['data']:
        assert w['workout_type'] == 'Running'

    res_sort = client.get('/api/workouts?sort_by=duration&order=desc')
    assert res_sort.status_code == 200
    durations = [w['duration'] for w in res_sort.get_json()['data']]
    assert durations == sorted(durations, reverse=True)
