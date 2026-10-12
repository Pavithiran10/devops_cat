import sqlite3
import os
from datetime import date, timedelta
from database.db import get_db

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_type TEXT NOT NULL,
    duration INTEGER NOT NULL,
    calories INTEGER NOT NULL,
    distance REAL DEFAULT 0,
    workout_date TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS daily_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_date TEXT NOT NULL UNIQUE,
    steps INTEGER DEFAULT 0,
    calories INTEGER DEFAULT 0,
    distance REAL DEFAULT 0,
    water_intake REAL DEFAULT 0,
    active_minutes INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY,
    daily_step_goal INTEGER DEFAULT 8000,
    weekly_workout_goal INTEGER DEFAULT 5,
    daily_water_goal REAL DEFAULT 2.5
);
"""

def init_db(db_path=None, force=False):
    """
    Initialize SQLite tables.
    If force is True, drops existing tables and recreates them.
    If the database is empty (no records in workouts/goals), seeds initial sample data.
    """
    conn = get_db(db_path)
    cursor = conn.cursor()

    if force:
        cursor.execute("DROP TABLE IF EXISTS workouts")
        cursor.execute("DROP TABLE IF EXISTS daily_activity")
        cursor.execute("DROP TABLE IF EXISTS goals")

    cursor.executescript(SCHEMA_SQL)
    conn.commit()

    # Check if database is empty
    cursor.execute("SELECT COUNT(*) FROM goals")
    goals_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM workouts")
    workouts_count = cursor.fetchone()[0]

    if goals_count == 0 or workouts_count == 0 or force:
        seed_sample_data(conn)

    cursor.close()
    return True

def seed_sample_data(conn):
    """
    Seed realistic initial fitness data relative to the current date.
    Ensures dashboard displays live weekly charts and summary stats out-of-the-box.
    """
    cursor = conn.cursor()

    # 1. Seed Goals (Single record id=1)
    cursor.execute("""
        INSERT OR REPLACE INTO goals (id, daily_step_goal, weekly_workout_goal, daily_water_goal)
        VALUES (1, 8000, 5, 2.5)
    """)

    # 2. Seed Daily Activity for the past 7 days (including today)
    today = date.today()
    sample_activities = [
        # (days_ago, steps, calories, distance_km, water_liters, active_minutes)
        (6, 7540, 2150, 5.2, 2.2, 45),
        (5, 9200, 2400, 6.8, 2.8, 60),
        (4, 6800, 1980, 4.7, 2.0, 40),
        (3, 10450, 2650, 7.9, 3.0, 75),
        (2, 8300, 2220, 5.9, 2.5, 50),
        (1, 11200, 2780, 8.4, 3.2, 80),
        (0, 8650, 2310, 6.1, 2.6, 55), # Today
    ]

    for days_ago, steps, cals, dist, water, active_min in sample_activities:
        act_date = (today - timedelta(days=days_ago)).isoformat()
        cursor.execute("""
            INSERT OR REPLACE INTO daily_activity 
            (activity_date, steps, calories, distance, water_intake, active_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (act_date, steps, cals, dist, water, active_min))

    # 3. Seed Sample Workouts across recent days
    sample_workouts = [
        ("Running", 45, 480, 5.5, (today - timedelta(days=6)).isoformat(), "Morning park trail run with steady pace."),
        ("Yoga", 30, 160, 0.0, (today - timedelta(days=5)).isoformat(), "Evening Vinyasa flow for flexibility and recovery."),
        ("Cycling", 50, 520, 14.2, (today - timedelta(days=4)).isoformat(), "Outdoor cycling circuit along scenic lake drive."),
        ("Strength Training", 60, 450, 0.0, (today - timedelta(days=3)).isoformat(), "Upper body push-pull routine, progressive overload."),
        ("Walking", 40, 210, 3.4, (today - timedelta(days=2)).isoformat(), "Brisk lunch walk around university campus."),
        ("Running", 35, 390, 4.6, (today - timedelta(days=1)).isoformat(), "Interval sprints: 5x 400m with jog recoveries."),
        ("Cycling", 45, 460, 12.8, today.isoformat(), "Mid-day aerobic ride, felt strong and energized."),
    ]

    for w_type, duration, calories, distance, w_date, notes in sample_workouts:
        # Check if identical workout already seeded
        cursor.execute("""
            SELECT id FROM workouts 
            WHERE workout_type = ? AND workout_date = ? AND duration = ?
        """, (w_type, w_date, duration))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO workouts (workout_type, duration, calories, distance, workout_date, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (w_type, duration, calories, distance, w_date, notes))

    conn.commit()
    cursor.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized and seeded successfully.")
