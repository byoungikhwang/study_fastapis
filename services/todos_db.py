import sqlite3

DATABASE_FILE = "todos.db"

def init_db():
    """Initializes the database and creates the todos table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    """Returns a new database connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    # Return rows that can be accessed by column name
    conn.row_factory = sqlite3.Row
    return conn
