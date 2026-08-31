import sqlite3
from contextlib import contextmanager

DB_NAME = "movies.db"


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY,
                title    TEXT    NOT NULL,
                director TEXT    NOT NULL,
                genre    TEXT    NOT NULL,
                duration INTEGER NOT NULL,
                rating   REAL    NOT NULL
            )
            """
        )
        conn.commit()


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
