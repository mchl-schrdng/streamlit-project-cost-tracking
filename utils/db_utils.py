import sqlite3
from datetime import datetime, timedelta

DB_PATH = "database.db"


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                daily_rate REAL NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                budget REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agenda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consultant_id INTEGER,
                project_id INTEGER NOT NULL,
                week INTEGER NOT NULL,
                start_date TEXT,
                end_date TEXT,
                days_worked INTEGER NOT NULL DEFAULT 0,
                actual_days_worked INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (consultant_id) REFERENCES consultants (id),
                FOREIGN KEY (project_id) REFERENCES projects (id)
            );
        """)
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.commit()
        conn.close()


def calculate_project_weeks(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    weeks = []

    while start <= end:
        week_start = start
        week_end = min(start + timedelta(days=6), end)
        weeks.append({
            "week": week_start.isocalendar()[1],
            "start_date": week_start.strftime("%Y-%m-%d"),
            "end_date": week_end.strftime("%Y-%m-%d"),
        })
        start += timedelta(days=7)

    return weeks


def get_consultants():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultants;")
        consultants = cursor.fetchall()
        conn.close()
        return [dict(row) for row in consultants]
    except sqlite3.OperationalError as e:
        print(f"Error fetching consultants: {e}")
        return []


def add_consultant(name, role, daily_rate):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO consultants (name, role, daily_rate)
            VALUES (?, ?, ?);
        """, (name, role, daily_rate))
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Error adding consultant: {e}")


def update_consultant(consultant_id, name, role, daily_rate):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE consultants
        SET name = ?, role = ?, daily_rate = ?
        WHERE id = ?;
    """, (name, role, daily_rate, consultant_id))
    conn.commit()
    conn.close()


def delete_consultant(consultant_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM consultants WHERE id = ?;
    """, (consultant_id,))
    conn.commit()
    conn.close()


def get_projects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects;")
    projects = cursor.fetchall()
    conn.close()
    return [dict(row) for row in projects]


def add_project(name, description, budget, start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projects (name, description, budget, start_date, end_date)
        VALUES (?, ?, ?, ?, ?);
    """, (name, description, budget, start_date, end_date))

    conn.commit()
    project_id = cursor.lastrowid

    weeks = calculate_project_weeks(start_date, end_date)
    for week in weeks:
        cursor.execute("""
            INSERT INTO agenda (project_id, week, start_date, end_date, days_worked, actual_days_worked)
            VALUES (?, ?, ?, ?, 0, 0);
        """, (project_id, week["week"], week["start_date"], week["end_date"]))

    conn.commit()
    conn.close()


def update_project(project_id, name, description, budget, start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projects
        SET name = ?, description = ?, budget = ?, start_date = ?, end_date = ?
        WHERE id = ?;
    """, (name, description, budget, start_date, end_date, project_id))
    conn.commit()
    conn.close()


def delete_project(project_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM projects WHERE id = ?;
    """, (project_id,))
    conn.commit()
    conn.close()


def get_agenda():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.consultant_id, a.project_id, a.week, a.start_date, a.end_date, a.days_worked, a.actual_days_worked,
               c.name AS consultant_name, p.name AS project_name
        FROM agenda a
        LEFT JOIN consultants c ON a.consultant_id = c.id
        JOIN projects p ON a.project_id = p.id;
    """)
    agenda = cursor.fetchall()
    conn.close()
    return [dict(row) for row in agenda]


def update_agenda(agenda_id, consultant_id=None, days_worked=None, actual_days_worked=None):
    conn = connect_db()
    cursor = conn.cursor()
    query = "UPDATE agenda SET "
    params = []
    if consultant_id is not None:
        query += "consultant_id = ?, "
        params.append(consultant_id)
    if days_worked is not None:
        query += "days_worked = ?, "
        params.append(days_worked)
    if actual_days_worked is not None:
        query += "actual_days_worked = ?, "
        params.append(actual_days_worked)
    query = query.rstrip(", ") + " WHERE id = ?"
    params.append(agenda_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()