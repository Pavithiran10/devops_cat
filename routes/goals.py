from flask import Blueprint, request, jsonify
from database.db import query_db, execute_db

goals_bp = Blueprint('goals', __name__, url_prefix='/api/goals')

def validate_goals_payload(data):
    """Validate user goals payload."""
    errors = []
    if not isinstance(data, dict):
        return ["Request payload must be a JSON object."]

    step_goal = data.get('daily_step_goal')
    if step_goal is not None:
        if not isinstance(step_goal, (int, float)) or int(step_goal) <= 0:
            errors.append("daily_step_goal must be a positive integer greater than 0.")

    weekly_goal = data.get('weekly_workout_goal')
    if weekly_goal is not None:
        if not isinstance(weekly_goal, (int, float)) or int(weekly_goal) <= 0:
            errors.append("weekly_workout_goal must be a positive integer greater than 0.")

    water_goal = data.get('daily_water_goal')
    if water_goal is not None:
        if not isinstance(water_goal, (int, float)) or float(water_goal) <= 0:
            errors.append("daily_water_goal must be a positive number greater than 0.")

    return errors

@goals_bp.route('', methods=['GET'])
def get_goals():
    """Retrieve user fitness goals."""
    goal = query_db("SELECT * FROM goals WHERE id = 1", one=True)
    if not goal:
        # Default fallback
        goal = {
            "id": 1,
            "daily_step_goal": 8000,
            "weekly_workout_goal": 5,
            "daily_water_goal": 2.5
        }
    return jsonify({
        "status": "success",
        "data": goal
    }), 200

@goals_bp.route('', methods=['PUT'])
def update_goals():
    """Update user fitness goals."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON request body."
        }), 400

    errors = validate_goals_payload(data)
    if errors:
        return jsonify({
            "status": "error",
            "message": "Validation failed.",
            "errors": errors
        }), 400

    current = query_db("SELECT * FROM goals WHERE id = 1", one=True)
    step_goal = int(data.get('daily_step_goal', current['daily_step_goal'] if current else 8000))
    weekly_goal = int(data.get('weekly_workout_goal', current['weekly_workout_goal'] if current else 5))
    water_goal = round(float(data.get('daily_water_goal', current['daily_water_goal'] if current else 2.5)), 2)

    execute_db(
        """
        INSERT INTO goals (id, daily_step_goal, weekly_workout_goal, daily_water_goal)
        VALUES (1, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            daily_step_goal = excluded.daily_step_goal,
            weekly_workout_goal = excluded.weekly_workout_goal,
            daily_water_goal = excluded.daily_water_goal
        """,
        (step_goal, weekly_goal, water_goal)
    )

    updated = query_db("SELECT * FROM goals WHERE id = 1", one=True)
    return jsonify({
        "status": "success",
        "message": "Goals updated successfully.",
        "data": updated
    }), 200
