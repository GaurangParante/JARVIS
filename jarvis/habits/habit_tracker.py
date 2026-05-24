"""Habit tracking logic for JARVIS."""

import json
from pathlib import Path
from datetime import datetime, timedelta

from database.db import run_query
from utils.time_utils import get_today_date


class HabitTracker:
    """Manage habit completion records and streaks."""

    def __init__(self):
        self.data_file = Path(__file__).resolve().parents[1] / "data" / "habits.json"
        self._ensure_default_habits_file()

    def _ensure_default_habits_file(self):
        """Create the default habit list file if it does not exist."""
        if self.data_file.exists():
            return

        default_data = {
            "default_habits": ["gym", "reading", "meditation", "walking"]
        }
        self.data_file.write_text(json.dumps(default_data, indent=4), encoding="utf-8")

    def mark_habit_completed(self, habit_name):
        """Record a habit completion and update the streak."""
        today = get_today_date()
        last_entry = run_query(
            """
            SELECT id, completed_date, streak_count
            FROM habits
            WHERE habit_name = ?
            ORDER BY completed_date DESC, id DESC
            LIMIT 1
            """,
            (habit_name,),
            fetchone=True,
        )

        if last_entry and last_entry[1] == today:
            return f"{habit_name.title()} is already marked completed for today."

        streak_count = self._calculate_streak(last_entry)

        run_query(
            """
            INSERT INTO habits (habit_name, completed_date, streak_count)
            VALUES (?, ?, ?)
            """,
            (habit_name, today, streak_count),
        )

        return f"{habit_name.title()} marked completed. Current streak is {streak_count}."

    def _calculate_streak(self, last_entry):
        """Calculate the next streak value."""
        if not last_entry:
            return 1

        last_completed_date = datetime.strptime(last_entry[1], "%Y-%m-%d").date()
        yesterday = datetime.now().date() - timedelta(days=1)

        if last_completed_date == yesterday:
            return last_entry[2] + 1

        return 1

    def get_habit_summary(self):
        """Return the latest record for each habit."""
        rows = run_query(
            """
            SELECT h1.habit_name, h1.completed_date, h1.streak_count
            FROM habits h1
            INNER JOIN (
                SELECT habit_name, MAX(id) AS latest_id
                FROM habits
                GROUP BY habit_name
            ) h2 ON h1.id = h2.latest_id
            ORDER BY h1.habit_name
            """,
            fetchall=True,
        )
        return rows

    def get_streak_summary(self):
        """Return current streaks for all habits."""
        rows = self.get_habit_summary()
        return [(habit_name, streak_count) for habit_name, _date, streak_count in rows]
