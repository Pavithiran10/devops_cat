from datetime import date, timedelta
from database.db import query_db

def get_dashboard_summary():
    """
    Computes dashboard KPIs:
    - Today's steps, distance, total calories (from activity + workouts),
      workout duration, water intake, daily step goal completion %,
      weekly activity chart data (last 7 days), and recent 5 workouts.
    """
    today_str = date.today().isoformat()
    seven_days_ago = (date.today() - timedelta(days=6)).isoformat()

    # 1. Fetch Goals
    goal_row = query_db("SELECT * FROM goals WHERE id = 1", one=True)
    if not goal_row:
        step_goal = 8000
        weekly_workout_goal = 5
        water_goal = 2.5
    else:
        step_goal = goal_row.get('daily_step_goal', 8000)
        weekly_workout_goal = goal_row.get('weekly_workout_goal', 5)
        water_goal = goal_row.get('daily_water_goal', 2.5)

    # 2. Today's Daily Activity
    today_activity = query_db(
        "SELECT * FROM daily_activity WHERE activity_date = ?",
        (today_str,),
        one=True
    )

    steps_today = today_activity.get('steps', 0) if today_activity else 0
    distance_today = today_activity.get('distance', 0.0) if today_activity else 0.0
    water_today = today_activity.get('water_intake', 0.0) if today_activity else 0.0
    activity_cals_today = today_activity.get('calories', 0) if today_activity else 0
    active_mins_today = today_activity.get('active_minutes', 0) if today_activity else 0

    # 3. Today's Workouts aggregation
    today_workouts_agg = query_db(
        """
        SELECT 
            COALESCE(SUM(duration), 0) AS total_duration,
            COALESCE(SUM(calories), 0) AS total_workout_calories,
            COALESCE(SUM(distance), 0.0) AS total_workout_distance,
            COUNT(*) AS workout_count
        FROM workouts
        WHERE workout_date = ?
        """,
        (today_str,),
        one=True
    )

    workout_duration_today = today_workouts_agg['total_duration']
    workout_cals_today = today_workouts_agg['total_workout_calories']
    workout_dist_today = round(today_workouts_agg['total_workout_distance'], 2)

    # Combine distance: if daily_activity recorded distance is 0, add workout distance
    effective_distance = max(distance_today, workout_dist_today) if distance_today > 0 else (distance_today + workout_dist_today)
    total_calories_today = max(activity_cals_today, activity_cals_today + workout_cals_today if activity_cals_today == 0 else activity_cals_today)

    step_goal_pct = min(100.0, round((steps_today / step_goal * 100), 1)) if step_goal > 0 else 0.0
    water_goal_pct = min(100.0, round((water_today / water_goal * 100), 1)) if water_goal > 0 else 0.0

    # 4. Weekly Workouts Count (last 7 days)
    weekly_workouts_res = query_db(
        "SELECT COUNT(*) AS cnt FROM workouts WHERE workout_date BETWEEN ? AND ?",
        (seven_days_ago, today_str),
        one=True
    )
    weekly_workout_count = weekly_workouts_res['cnt'] if weekly_workouts_res else 0
    weekly_workout_pct = min(100.0, round((weekly_workout_count / weekly_workout_goal * 100), 1)) if weekly_workout_goal > 0 else 0.0

    # 5. Weekly Chart Data (Daily steps & calories for the past 7 days)
    # Generate continuous dates
    dates_list = [(date.today() - timedelta(days=i)).isoformat() for i in reversed(range(7))]
    activities_rows = query_db(
        "SELECT * FROM daily_activity WHERE activity_date BETWEEN ? AND ? ORDER BY activity_date ASC",
        (seven_days_ago, today_str)
    )
    act_map = {row['activity_date']: row for row in activities_rows}

    # Also sum workout calories per date
    workout_cal_rows = query_db(
        """
        SELECT workout_date, SUM(calories) as sum_cals
        FROM workouts
        WHERE workout_date BETWEEN ? AND ?
        GROUP BY workout_date
        """,
        (seven_days_ago, today_str)
    )
    w_cal_map = {row['workout_date']: row['sum_cals'] for row in workout_cal_rows}

    weekly_labels = []
    weekly_steps = []
    weekly_calories = []

    for d in dates_list:
        parsed_d = date.fromisoformat(d)
        weekly_labels.append(parsed_d.strftime('%a (%m/%d)'))
        act = act_map.get(d)
        st = act['steps'] if act else 0
        cal = act['calories'] if act else 0
        w_cal = w_cal_map.get(d, 0)
        # Combine or fallback
        total_day_cal = cal if cal > 0 else w_cal
        weekly_steps.append(st)
        weekly_calories.append(total_day_cal)

    # 6. Recent Workouts (up to 5)
    recent_workouts = query_db(
        "SELECT * FROM workouts ORDER BY workout_date DESC, id DESC LIMIT 5"
    )

    return {
        "today": {
            "date": today_str,
            "steps": steps_today,
            "distance_km": round(effective_distance, 2),
            "calories": total_calories_today,
            "workout_duration_minutes": workout_duration_today,
            "water_intake_liters": round(water_today, 2),
            "active_minutes": active_mins_today,
            "step_goal": step_goal,
            "step_goal_pct": step_goal_pct,
            "water_goal": water_goal,
            "water_goal_pct": water_goal_pct,
            "weekly_workout_count": weekly_workout_count,
            "weekly_workout_goal": weekly_workout_goal,
            "weekly_workout_pct": weekly_workout_pct
        },
        "weekly_chart": {
            "labels": weekly_labels,
            "steps": weekly_steps,
            "calories": weekly_calories
        },
        "recent_workouts": recent_workouts
    }

def get_detailed_analytics():
    """
    Computes comprehensive analytics:
    - Weekly steps
    - Daily calorie expenditure
    - Workout distribution by type
    - Total workouts completed
    - Average workout duration
    - Daily and weekly goal completion rates
    """
    today_str = date.today().isoformat()
    seven_days_ago = (date.today() - timedelta(days=6)).isoformat()

    # 1. Total workouts & Averages
    overall_stats = query_db(
        """
        SELECT 
            COUNT(*) AS total_workouts,
            COALESCE(AVG(duration), 0.0) AS avg_duration,
            COALESCE(SUM(calories), 0) AS total_calories,
            COALESCE(SUM(distance), 0.0) AS total_distance
        FROM workouts
        """,
        one=True
    )

    # 2. Workout distribution by type
    dist_rows = query_db(
        """
        SELECT 
            workout_type,
            COUNT(*) AS count,
            COALESCE(SUM(duration), 0) AS total_minutes,
            COALESCE(SUM(calories), 0) AS total_calories
        FROM workouts
        GROUP BY workout_type
        ORDER BY count DESC
        """
    )

    total_w = overall_stats['total_workouts'] or 1
    distribution = []
    type_labels = []
    type_counts = []
    for r in dist_rows:
        pct = round((r['count'] / total_w) * 100, 1)
        type_labels.append(r['workout_type'])
        type_counts.append(r['count'])
        distribution.append({
            "workout_type": r['workout_type'],
            "count": r['count'],
            "percentage": pct,
            "total_minutes": r['total_minutes'],
            "total_calories": r['total_calories']
        })

    # 3. Weekly Trends
    dashboard_sum = get_dashboard_summary()

    # 4. Goals and completion status
    goals = query_db("SELECT * FROM goals WHERE id = 1", one=True) or {
        "daily_step_goal": 8000,
        "weekly_workout_goal": 5,
        "daily_water_goal": 2.5
    }

    return {
        "total_workouts": overall_stats['total_workouts'],
        "avg_duration_minutes": round(overall_stats['avg_duration'], 1),
        "total_calories_burned": overall_stats['total_calories'],
        "total_distance_km": round(overall_stats['total_distance'], 2),
        "distribution": distribution,
        "distribution_chart": {
            "labels": type_labels,
            "counts": type_counts
        },
        "weekly_trends": dashboard_sum['weekly_chart'],
        "goals": goals,
        "completion_rates": {
            "daily_step_goal_pct": dashboard_sum['today']['step_goal_pct'],
            "weekly_workout_goal_pct": dashboard_sum['today']['weekly_workout_pct'],
            "daily_water_goal_pct": dashboard_sum['today']['water_goal_pct']
        }
    }
