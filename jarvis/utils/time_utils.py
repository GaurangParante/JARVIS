"""Time helper functions for JARVIS."""

from datetime import datetime


def get_current_time_text():
    """Return the current time as a friendly sentence."""
    current_time = datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}."


def get_today_date():
    """Return today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")
