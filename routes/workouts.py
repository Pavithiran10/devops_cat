import re
from datetime import datetime
from flask import Blueprint, request, jsonify
from database.db import query_db, execute_db

workouts_bp = Blueprint('workouts', __name__, url_prefix='/api/workouts')

VALID_WORKOUT_TYPES = ["Running", "Walking", "Cycling", "Strength Training", "Yoga"]

def validate_workout_payload(data, is_update=False):
    """Validate JSON payload for workout creation and updates."""
    errors = []

    if not isinstance(data, dict):
        return ["Request payload must be a JSON object."]

    workout_type = data.get('workout_type')
    if workout_type is not None or not is_update:
        if not workout_type or workout_type not in VALID_WORKOUT_TYPES:
            errors.append(f"workout_type must be one of: {', '.join(VALID_WORKOUT_TYPES)}")

    duration = data.get('duration')
    if duration is not None or not is_update:
        if duration is None or not isinstance(duration, (int, float)) or int(duration) <= 0:
            errors.append("duration must be a positive integer greater than 0.")

    calories = data.get('calories')
    if calories is not None or not is_update:
        if calories is None or not isinstance(calories, (int, float)) or int(calories) < 0:
            errors.append("calories must be an integer greater than or equal to 0.")

    distance = data.get('distance')
    if distance is not None:
        if not isinstance(distance, (int, float)) or float(distance) < 0:
            errors.append("distance must be a non-negative number.")

    workout_date = data.get('workout_date')
    if workout_date is not None or not is_update:
        if not workout_date or not isinstance(workout_date, str):
            errors.append("workout_date is required in YYYY-MM-DD format.")
        else:
            try:
                datetime.strptime(workout_date, "%Y-%m-%d")
            except ValueError:
                errors.append("workout_date must be formatted as YYYY-MM-DD.")

    return errors

@workouts_bp.route('', methods=['GET'])
def get_all_workouts():
    """Retrieve workouts with search, filter by type/date, and sorting."""
    workout_type = request.args.get('type')
    date_val = request.args.get('date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'workout_date')
    order = request.args.get('order', 'desc').lower()

    valid_sort_fields = {
        'id': 'id',
        'workout_date': 'workout_date',
        'duration': 'duration',
        'calories': 'calories',
        'distance': 'distance',
        'workout_type': 'workout_type'
    }
    sort_col = valid_sort_fields.get(sort_by, 'workout_date')
    direction = 'ASC' if order == 'asc' else 'DESC'

    query = "SELECT * FROM workouts WHERE 1=1"
    params = []

    if workout_type and workout_type.strip():
        query += " AND workout_type = ?"
        params.append(workout_type.strip())

    if date_val and date_val.strip():
        query += " AND workout_date = ?"
        params.append(date_val.strip())

    if start_date and start_date.strip():
        query += " AND workout_date >= ?"
        params.append(start_date.strip())

    if end_date and end_date.strip():
        query += " AND workout_date <= ?"
        params.append(end_date.strip())

    if search and search.strip():
        query += " AND (notes LIKE ? OR workout_type LIKE ?)"
        pattern = f"%{search.strip()}%"
        params.extend([pattern, pattern])

    # Append safe order clause
    query += f" ORDER BY {sort_col} {direction}, id {direction}"

    workouts = query_db(query, tuple(params))
    return jsonify({
        "status": "success",
        "count": len(workouts),
        "data": workouts
    }), 200

@workouts_bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    """Retrieve a single workout by its ID."""
    workout = query_db("SELECT * FROM workouts WHERE id = ?", (workout_id,), one=True)
    if not workout:
        return jsonify({
            "status": "error",
            "message": f"Workout with ID {workout_id} not found."
        }), 404
    return jsonify({
        "status": "success",
        "data": workout
    }), 200

@workouts_bp.route('', methods=['POST'])
def create_workout():
    """Create a new workout record."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON request body."
        }), 400

    errors = validate_workout_payload(data)
    if errors:
        return jsonify({
            "status": "error",
            "message": "Validation failed.",
            "errors": errors
        }), 400

    workout_type = data['workout_type'].strip()
    duration = int(data['duration'])
    calories = int(data['calories'])
    distance = round(float(data.get('distance', 0.0)), 2)
    workout_date = data['workout_date'].strip()
    notes = data.get('notes', '').strip() if data.get('notes') else ''

    last_id, _ = execute_db(
        """
        INSERT INTO workouts (workout_type, duration, calories, distance, workout_date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (workout_type, duration, calories, distance, workout_date, notes)
    )

    created_workout = query_db("SELECT * FROM workouts WHERE id = ?", (last_id,), one=True)
    return jsonify({
        "status": "success",
        "message": "Workout created successfully.",
        "data": created_workout
    }), 201

@workouts_bp.route('/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    """Update an existing workout."""
    existing = query_db("SELECT * FROM workouts WHERE id = ?", (workout_id,), one=True)
    if not existing:
        return jsonify({
            "status": "error",
            "message": f"Workout with ID {workout_id} not found."
        }), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON request body."
        }), 400

    errors = validate_workout_payload(data, is_update=True)
    if errors:
        return jsonify({
            "status": "error",
            "message": "Validation failed.",
            "errors": errors
        }), 400

    workout_type = data.get('workout_type', existing['workout_type']).strip()
    duration = int(data.get('duration', existing['duration']))
    calories = int(data.get('calories', existing['calories']))
    distance = round(float(data.get('distance', existing['distance'])), 2)
    workout_date = data.get('workout_date', existing['workout_date']).strip()
    notes = data.get('notes', existing['notes'])
    if notes is not None:
        notes = notes.strip()

    execute_db(
        """
        UPDATE workouts
        SET workout_type = ?, duration = ?, calories = ?, distance = ?, workout_date = ?, notes = ?
        WHERE id = ?
        """,
        (workout_type, duration, calories, distance, workout_date, notes, workout_id)
    )

    updated_workout = query_db("SELECT * FROM workouts WHERE id = ?", (workout_id,), one=True)
    return jsonify({
        "status": "success",
        "message": "Workout updated successfully.",
        "data": updated_workout
    }), 200

@workouts_bp.route('/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout by ID."""
    existing = query_db("SELECT * FROM workouts WHERE id = ?", (workout_id,), one=True)
    if not existing:
        return jsonify({
            "status": "error",
            "message": f"Workout with ID {workout_id} not found."
        }), 404

    execute_db("DELETE FROM workouts WHERE id = ?", (workout_id,))
    return jsonify({
        "status": "success",
        "message": f"Workout with ID {workout_id} deleted successfully."
    }), 200
