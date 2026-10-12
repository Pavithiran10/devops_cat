import os
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, send_from_directory, request
from config import config_by_name, Config
from database.db import init_app, query_db
from database.init_db import init_db
from routes.workouts import workouts_bp
from routes.activity import activity_bp
from routes.goals import goals_bp
from routes.dashboard import dashboard_bp

def create_app(config_class=None):
    """
    Application factory for FitTrack Flask application.
    """
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

    # Determine configuration
    if config_class is None:
        env_name = os.environ.get('FLASK_ENV', 'default')
        config_class = config_by_name.get(env_name, Config)

    app.config.from_object(config_class)

    # Register database teardown
    init_app(app)

    # Initialize database tables and sample data if not in test mode
    with app.app_context():
        if not app.config.get('TESTING', False):
            init_db()

    # Register API Blueprints
    app.register_blueprint(workouts_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(dashboard_bp)

    # Health Check Endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint for Docker, Jenkins, and container orchestration.
        Verifies SQLite database connectivity.
        """
        try:
            # Test database query
            db_check = query_db("SELECT 1 AS alive", one=True)
            db_status = "connected" if db_check and db_check.get('alive') == 1 else "unhealthy"
            return jsonify({
                "status": "healthy",
                "app": "FitTrack",
                "version": "1.0.0",
                "database": db_status,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 503

    # Frontend Single-Page Application (SPA) Route
    @app.route('/')
    @app.route('/workouts')
    @app.route('/add-workout')
    @app.route('/activity')
    @app.route('/analytics')
    @app.route('/goals')
    def index():
        """Serve the frontend single page application."""
        return render_template('index.html')

    # Centralized Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith('/api/'):
            return jsonify({"status": "error", "message": "Bad Request", "details": str(error)}), 400
        return render_template('index.html'), 400

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({"status": "error", "message": "Resource not found."}), 404
        # For browser navigation, fallback to SPA index
        return render_template('index.html'), 200

    @app.errorhandler(405)
    def method_not_allowed(error):
        if request.path.startswith('/api/'):
            return jsonify({"status": "error", "message": "Method not allowed for this endpoint."}), 405
        return render_template('index.html'), 405

    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith('/api/'):
            return jsonify({"status": "error", "message": "Internal server error."}), 500
        return render_template('index.html'), 500

    return app

# WSGI Application Entry Point
app = create_app()

if __name__ == '__main__':
    port = app.config.get('PORT', 5000)
    host = app.config.get('HOST', '0.0.0.0')
    debug = app.config.get('DEBUG', False)
    app.run(host=host, port=port, debug=debug)
