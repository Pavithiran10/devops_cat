import sqlite3
import os
from flask import g, current_app

def get_db(db_path=None):
    """
    Get a database connection.
    If running within a Flask application context, store the connection on Flask's 'g'.
    Otherwise, open and return a standalone connection.
    """
    # Check if we are inside an active Flask application context
    if current_app:
        target_path = db_path or current_app.config.get('DATABASE_PATH', 'fittrack.db')
        if 'db' not in g:
            # Ensure parent directory exists for file-based databases
            if target_path != ':memory:':
                parent_dir = os.path.dirname(target_path)
                if parent_dir:
                    os.makedirs(parent_dir, exist_ok=True)
            g.db = sqlite3.connect(target_path)
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
        return g.db

    # Standalone usage (e.g. CLI scripts or background workers)
    target_path = db_path or os.environ.get('DATABASE_PATH', 'fittrack.db')
    if target_path != ':memory:':
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def close_db(e=None):
    """Close the database connection registered in Flask's 'g' context."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Register database teardown with Flask application."""
    app.teardown_appcontext(close_db)

def query_db(query, args=(), one=False, db_path=None):
    """
    Execute a parameterized SQL SELECT query and return results as dictionaries.
    """
    conn = get_db(db_path)
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    if not current_app and db_path != ':memory:':
        # Don't leave connection dangling in standalone mode
        conn.close()
    results = [dict(row) for row in rv]
    return (results[0] if results else None) if one else results

def execute_db(query, args=(), db_path=None):
    """
    Execute a parameterized INSERT/UPDATE/DELETE query within a transaction.
    Returns (lastrowid, rowcount).
    """
    conn = get_db(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        conn.commit()
        last_id = cursor.lastrowid
        rowcount = cursor.rowcount
        cursor.close()
        if not current_app and db_path != ':memory:':
            conn.close()
        return last_id, rowcount
    except Exception as e:
        conn.rollback()
        cursor.close()
        if not current_app and db_path != ':memory:':
            conn.close()
        raise e
