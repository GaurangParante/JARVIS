"""Todo feature logic for JARVIS."""

from database.db import run_query
from utils.time_utils import get_today_date


class TodoManager:
    """Manage todo tasks stored in SQLite."""

    def add_task(self, task_name, task_date, task_time):
        """Insert a new task into the database."""
        run_query(
            """
            INSERT INTO todos (task_name, task_date, task_time, status)
            VALUES (?, ?, ?, 'pending')
            """,
            (task_name, task_date, task_time),
        )

    def get_pending_tasks(self):
        """Return all pending tasks."""
        return run_query(
            """
            SELECT id, task_name, task_date, task_time
            FROM todos
            WHERE status = 'pending'
            ORDER BY task_date, task_time
            """,
            fetchall=True,
        )

    def get_today_pending_count(self):
        """Return the number of pending tasks for today."""
        result = run_query(
            """
            SELECT COUNT(*)
            FROM todos
            WHERE status = 'pending' AND task_date = ?
            """,
            (get_today_date(),),
            fetchone=True,
        )
        return result[0] if result else 0

    def complete_task(self, task_id):
        """Mark a pending task as completed."""
        existing = run_query(
            """
            SELECT id
            FROM todos
            WHERE id = ? AND status = 'pending'
            """,
            (task_id,),
            fetchone=True,
        )

        if not existing:
            return False

        run_query(
            """
            UPDATE todos
            SET status = 'completed'
            WHERE id = ?
            """,
            (task_id,),
        )
        return True

    def delete_task(self, task_id):
        """Delete a task from the database."""
        existing = run_query(
            "SELECT id FROM todos WHERE id = ?",
            (task_id,),
            fetchone=True,
        )

        if not existing:
            return False

        run_query("DELETE FROM todos WHERE id = ?", (task_id,))
        return True
