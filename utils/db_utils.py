import sqlite3

# Database connection
DB_PATH = "database.db"  # Path to SQLite database


def connect_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access
    return conn


def init_db():
    """Initialize the database with necessary tables."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Consultants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            daily_rate REAL NOT NULL
        );
    """)
    
    # Projects table
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
    
    # Agenda table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultant_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            week INTEGER NOT NULL,
            days_worked INTEGER NOT NULL,
            actual_days_worked INTEGER DEFAULT 0,
            FOREIGN KEY (consultant_id) REFERENCES consultants (id),
            FOREIGN KEY (project_id) REFERENCES projects (id)
        );
    """)
    
    conn.commit()
    conn.close()


# CRUD Operations

# Consultants
def add_consultant(name, role, daily_rate):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO consultants (name, role, daily_rate)
        VALUES (?, ?, ?);
    """, (name, role, daily_rate))
    conn.commit()
    conn.close()


def get_consultants():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consultants;")
    consultants = cursor.fetchall()
    conn.close()
    return [dict(row) for row in consultants]


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
    cursor.execute("DELETE FROM consultants WHERE id = ?;", (consultant_id,))
    conn.commit()
    conn.close()


# Projects
def add_project(name, description, budget, start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projects (name, description, budget, start_date, end_date)
        VALUES (?, ?, ?, ?, ?);
    """, (name, description, budget, start_date, end_date))
    conn.commit()
    conn.close()


def get_projects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects;")
    projects = cursor.fetchall()
    conn.close()
    return [dict(row) for row in projects]


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
    cursor.execute("DELETE FROM projects WHERE id = ?;", (project_id,))
    conn.commit()
    conn.close()


# Agenda
def add_agenda(consultant_id, project_id, week, days_worked):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agenda (consultant_id, project_id, week, days_worked)
        VALUES (?, ?, ?, ?);
    """, (consultant_id, project_id, week, days_worked))
    conn.commit()
    conn.close()


def get_agenda():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.consultant_id, a.project_id, a.week, a.days_worked, a.actual_days_worked,
               c.name AS consultant_name, p.name AS project_name
        FROM agenda a
        JOIN consultants c ON a.consultant_id = c.id
        JOIN projects p ON a.project_id = p.id;
    """)
    agenda = cursor.fetchall()
    conn.close()
    return [dict(row) for row in agenda]


def update_agenda(agenda_id, consultant_id=None, project_id=None, week=None, days_worked=None, actual_days_worked=None):
    """
    Update an agenda entry. Only updates the fields that are not None.
    """
    conn = connect_db()
    cursor = conn.cursor()
    # Build dynamic query based on provided values
    query = "UPDATE agenda SET "
    updates = []
    params = []

    if consultant_id is not None:
        updates.append("consultant_id = ?")
        params.append(consultant_id)
    if project_id is not None:
        updates.append("project_id = ?")
        params.append(project_id)
    if week is not None:
        updates.append("week = ?")
        params.append(week)
    if days_worked is not None:
        updates.append("days_worked = ?")
        params.append(days_worked)
    if actual_days_worked is not None:
        updates.append("actual_days_worked = ?")
        params.append(actual_days_worked)

    query += ", ".join(updates) + " WHERE id = ?"
    params.append(agenda_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()


def delete_agenda(agenda_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agenda WHERE id = ?;", (agenda_id,))
    conn.commit()
    conn.close()