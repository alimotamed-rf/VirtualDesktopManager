import sys
import sqlite3
from pathlib import Path
from datetime import date


def get_base_directory():
    """
    Return the directory where persistent application data should live.

    Development:
        C:\WorkLogger

    PyInstaller EXE:
        directory containing the EXE
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


BASE_DIR = get_base_directory()

DATABASE_FILE = BASE_DIR / "tracker.db"


def get_connection():
    """Create a connection to the SQLite database."""

    return sqlite3.connect(DATABASE_FILE)


def create_database():
    """Create the database and required table."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS desktop_time (
            date TEXT NOT NULL,
            desktop_name TEXT NOT NULL,
            total_seconds REAL NOT NULL DEFAULT 0,
            PRIMARY KEY (date, desktop_name)
        )
    """)

    connection.commit()
    connection.close()


def add_time(desktop_name, seconds):
    """
    Add elapsed seconds to a desktop for today.
    """

    if seconds <= 0:
        return

    today = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO desktop_time
            (date, desktop_name, total_seconds)
        VALUES
            (?, ?, ?)

        ON CONFLICT(date, desktop_name)
        DO UPDATE SET
            total_seconds =
                total_seconds + excluded.total_seconds
    """, (
        today,
        desktop_name,
        seconds
    ))

    connection.commit()
    connection.close()


def get_today_totals():
    """Return today's accumulated time."""

    today = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT desktop_name, total_seconds
        FROM desktop_time
        WHERE date = ?
        ORDER BY desktop_name
    """, (today,))

    results = cursor.fetchall()

    connection.close()

    return results


def get_all_totals():
    """
    Return the complete tracking history.

    Result:
        [
            (date, desktop_name, total_seconds),
            ...
        ]
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            date,
            desktop_name,
            total_seconds
        FROM desktop_time
        ORDER BY
            date DESC,
            desktop_name
    """)

    results = cursor.fetchall()

    connection.close()

    return results


if __name__ == "__main__":

    create_database()

    print("Database ready:")
    print(DATABASE_FILE)