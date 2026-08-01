import sqlite3
from pathlib import Path

DB_PATH = Path("tasks.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            """
            INSERT INTO tasks(title, completed)
            VALUES (?, ?)
            """,
            [
                ("Learn FastAPI", False),
                ("Build CRUD API", False),
                ("Read FastAPI Docs", False),
            ],
        )

    conn.commit()
    conn.close()