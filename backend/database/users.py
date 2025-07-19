# backend/database/users.py
import sqlite3
from .schema import DB_NAME

def get_or_create_user(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    if row:
        user_id = row[0]
    else:
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        user_id = c.lastrowid
        conn.commit()

    conn.close()
    return user_id

# function used for testing purposes
def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, username FROM users")
    users = [{"id": row[0], "username": row[1]} for row in c.fetchall()]
    conn.close()
    return users