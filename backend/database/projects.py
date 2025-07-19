 # save/load project

# backend/database/projects.py
import sqlite3
from .schema import DB_NAME

def save_project(user_id, project_name, filters_json):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO projects (user_id, project_name, filters)
        VALUES (?, ?, ?)
    ''', (user_id, project_name, filters_json))
    conn.commit()
    conn.close()

def get_user_projects(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, project_name FROM projects WHERE user_id = ?", (user_id,))
    results = c.fetchall()
    conn.close()
    return results

def load_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT filters FROM projects WHERE id = ?", (project_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
