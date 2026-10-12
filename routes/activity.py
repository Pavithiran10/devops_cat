from datetime import date, datetime
from flask import Blueprint, request, jsonify
from database.db import query_db, execute_db

activity_bp = Blueprint('activity', __name__, url_prefix='/api/activity')

def validate_activity_payload(data):
    """Validate JSON payload for daily activity tracking."""
    errors = []
    if not isinstance(data, dict):
        return ["Request body must be a valid JSON object."]

    activity_date = data.get('activity_date')
    if activity_date:
        try:
            datetime.strptime(activity_date, "%Y-%m-%d")
        except ValueError:
            errors.append("activity_date must be formatted as YYYY-MM-DD.")

    steps = data.get('steps')
    if steps is not None:
        if not isinstance(steps, (int, float)) or int(steps) < 0:
            errors.append("steps must be a non-negative integer.")

    calories = data.get('calories')
    if calories is not None:
        if not isinstance(calories, (int, float)) or int(calories) < 0:
            errors.append("calories must be a non-negative integer.")

    distance = data.get('distance')
    if distance is not None:
        if not isinstance(distance, (int, float)) or float(distance) < 0:
            errors.append("distance must be a non-negative number.")

    water_intake = data.get('water_intake')
    if water_intake is not None:
        if not isinstance(water_intake, (int, float)) or float(water_intake) < 0:
            errors.append("water_intake must be a non-negative number.")

    active_minutes = data.get('active_minutes')
    if active_minutes is not None:
        if not isinstance(active_minutes, (int, float)) or int(active_minutes) < 0:
            errors.append("active_minutes must be a non-negative integer.")

    return errors

@activity_bp.route('', methods=['GET'])
def get_activity():
    """
    Retrieve activity records.
    Query params:
    - date: YYYY-MM-DD for single date record
    - limit: maximum records to return (default 30)
    """
    date_param = request.args.get('date')
    if date_param:
        try:
            datetime.strptime(date_param, "%Y-%m-%d")
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Invalid date format. Use YYYY-MM-DD."
            }), 400

        record = query_db(
            "SELECT * FROM daily_activity WHERE activity_date = ?",
            (date_param,),
            one=True
        )
        return jsonify({
            "status": "success",
            "data": record
        }), 200

    limit = request.args.get('limit', 30, type=int)
    records = query_db(
        "SELECT * FROM daily_activity ORDER BY activity_date DESC LIMIT ?",
        (limit,)
    )
    return jsonify({
        "status": "success",
        "count": len(records),
        "data": records
    }), 200

@activity_bp.route('', methods=['POST'])
def save_activity():
    """
    Create or update daily activity record for a given date.
    If activity_date is not provided, defaults to today.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON request body."
        }), 400

    errors = validate_activity_payload(data)
    if errors:
        return jsonify({
            "status": "error",
            "message": "Validation failed.",
            "errors": errors
        }), 400

    target_date = data.get('activity_date', date.today().isoformat())
    existing = query_db(
        "SELECT * FROM daily_activity WHERE activity_date = ?",
        (target_date,),
        one=True
    )

    steps = int(data.get('steps', existing['steps'] if existing else 0))
    calories = int(data.get('calories', existing['calories'] if existing else 0))
    distance = round(float(data.get('distance', existing['distance'] if existing else 0.0)), 2)
    water_intake = round(float(data.get('water_intake', existing['water_intake'] if existing else 0.0)), 2)
    active_minutes = int(data.get('active_minutes', existing['active_minutes'] if existing else 0))

    if existing:
        execute_db(
            """
            UPDATE daily_activity
            SET steps = ?, calories = ?, distance = ?, water_intake = ?, active_minutes = ?
            WHERE activity_date = ?
            """,
            (steps, calories, distance, water_intake, active_minutes, target_date)
        )
        status_code = 200
        msg = f"Activity record for {target_date} updated successfully."
    else:
        execute_db(
            """
            INSERT INTO daily_activity (activity_date, steps, calories, distance, water_intake, active_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (target_date, steps, calories, distance, water_intake, active_minutes)
        )
        status_code = 201
        msg = f"Activity record for {target_date} created successfully."

    updated_record = query_db(
        "SELECT * FROM daily_activity WHERE activity_date = ?",
        (target_date,),
        one=True
    )

    return jsonify({
        "status": "success",
        "message": msg,
        "data": updated_record
    }), status_code
