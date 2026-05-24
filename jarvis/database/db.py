"""Database helper functions for the JARVIS project."""

import sqlite3
from pathlib import Path


# Store the database beside this file inside the database folder.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "jarvis.db"


def get_connection():
    """Create and return a SQLite connection."""
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create the required tables if they do not already exist."""
    connection = get_connection()
    cursor = connection.cursor()

    # Create the todos table for storing task data.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            task_date TEXT NOT NULL,
            task_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )
        """
    )

    # Create the habits table for storing daily habit completion.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            completed_date TEXT NOT NULL,
            streak_count INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    connection.commit()
    connection.close()


def run_query(query, params=(), fetchone=False, fetchall=False):
    """Run a database query and optionally return rows."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()

    result = None

    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()

    connection.close()
    return result
