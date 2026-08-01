import psycopg2
import time
from app.config import DATABASE_URL

def get_connection():
    retries = 10

    while retries > 0:
        try:
            return psycopg2.connect(DATABASE_URL)
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)

    raise Exception("Could not connect to PostgreSQL")


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        );
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks;")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            """
            INSERT INTO tasks (title, completed)
            VALUES (%s, %s)
            """,
            [
                ("Learn FastAPI", False),
                ("Build CRUD API", False),
                ("Read FastAPI Docs", False),
            ]
        )

    conn.commit()

    cursor.close()
    conn.close()