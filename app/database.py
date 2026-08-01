import psycopg2

from app.config import DATABASE_URL


def get_connection():
    return psycopg2.connect(DATABASE_URL)


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