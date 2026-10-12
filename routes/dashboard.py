from flask import Blueprint, jsonify
from services.analytics import get_dashboard_summary, get_detailed_analytics
from database.init_db import init_db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api')

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Retrieve summarized dashboard metrics for today and the past 7 days."""
    try:
        summary = get_dashboard_summary()
        return jsonify({
            "status": "success",
            "data": summary
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to compute dashboard metrics: {str(e)}"
        }), 500

@dashboard_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Retrieve comprehensive analytics data for charts, distributions, and averages."""
    try:
        analytics_data = get_detailed_analytics()
        return jsonify({
            "status": "success",
            "data": analytics_data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to compute analytics data: {str(e)}"
        }), 500

@dashboard_bp.route('/reset', methods=['POST'])
def reset_demo_data():
    """Reset database to initial demo state with fresh sample records."""
    try:
        init_db(force=True)
        return jsonify({
            "status": "success",
            "message": "FitTrack demo data reset successfully."
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to reset demo data: {str(e)}"
        }), 500
