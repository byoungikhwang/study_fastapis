import psycopg2
from psycopg2.extras import DictCursor
from fastapi import Depends
from typing import Any
from config import settings

def get_db_connection():
    """Creates a new database connection."""
    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password
    )
    return conn

def init_db():
    """Initializes the PostgreSQL database and creates the notices table if it doesn't exist."""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Read notices.sql from the querys directory
            with open("querys/notices.sql", "r") as f:
                sql_script = f.read()
            cursor.execute(sql_script)
            conn.commit()
    except Exception as e:
        print(f"Error initializing notices database: {e}")
        # Depending on desired behavior, could re-raise or log more extensively
    finally:
        if conn:
            conn.close()

def get_db():
    """
    FastAPI dependency that provides a database connection with a DictCursor.
    The connection is automatically closed after the request is finished.
    """
    conn = None
    try:
        conn = get_db_connection()
        yield conn
    finally:
        if conn:
            conn.close()

# A dependency for a cursor, which is what we actually use to execute queries.
def get_cursor(conn: Any = Depends(get_db)):
    """
    FastAPI dependency that provides a DictCursor from a connection.
    """
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        yield cursor
