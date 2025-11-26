import psycopg2
from psycopg2.extras import DictCursor
from fastapi import Depends
from .config import settings

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
def get_cursor(conn: Depends(get_db)):
    """
    FastAPI dependency that provides a DictCursor from a connection.
    """
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        yield cursor
