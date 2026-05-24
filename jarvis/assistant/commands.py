"""Command processing logic for JARVIS."""

from utils.time_utils import get_current_time_text, get_today_date
from utils.settings_manager import load_settings, save_settings


class CommandProcessor:
    """Map user commands to assistant actions."""

    def __init__(self, todo_manager, habit_tracker, listener, speaker):
        self.todo_manager = todo_manager
        self.habit_tracker = habit_tracker
        self.listener = listener
        self.speaker = speaker
        self.settings = load_settings()

    def process(self, command):
        """
        Process a command and return a response dictionary.

        Returns:
            dict: A result with a text message and exit flag.
        """
        self.settings = load_settings()
        clean_command = command.strip().lower()

        if not clean_command:
            return {"message": self._message("empty_command"), "exit": False}

        if clean_command in {"help", "show commands", "what can you do"}:
            return {"message": self.get_supported_commands_text(), "exit": False}

        if clean_command in {"set language hindi", "set style hindi", "hindi mode"}:
            self._save_style("hindi")
            return {"message": self._message("language_hindi"), "exit": False}

        if clean_command in {"set language english", "set style english", "english mode"}:
            self._save_style("english")
            return {"message": self._message("language_english"), "exit": False}

        if clean_command in {"set voice zira", "female voice"}:
            return {"message": self._set_voice("Microsoft Zira Desktop"), "exit": False}

        if clean_command in {"set voice david", "male voice"}:
            return {"message": self._set_voice("Microsoft David Desktop"), "exit": False}

        if clean_command in {"set voice hazel"}:
            return {"message": self._set_voice("Microsoft Hazel Desktop"), "exit": False}

        if "what time is it" in clean_command or "tell me time" in clean_command:
            return {"message": self._time_message(), "exit": False}

        if clean_command == "add todo":
            return {"message": self._handle_add_todo(), "exit": False}

        if "show pending tasks" in clean_command:
            return {"message": self._handle_show_pending_tasks(), "exit": False}

        if "complete task" in clean_command:
            return {"message": self._handle_complete_task(), "exit": False}

        if "delete task" in clean_command:
            return {"message": self._handle_delete_task(), "exit": False}

        if clean_command.startswith("mark ") and clean_command.endswith(" completed"):
            return {"message": self._handle_mark_habit(clean_command), "exit": False}

        if "show habits" in clean_command:
            return {"message": self._handle_show_habits(), "exit": False}

        if "show streak" in clean_command:
            return {"message": self._handle_show_streaks(), "exit": False}

        if clean_command in {"exit", "stop jarvis"}:
            return {"message": self._message("exit"), "exit": True}

        return {"message": self._message("unknown_command"), "exit": False}

    def get_supported_commands_text(self):
        """Return a beginner-friendly list of supported commands."""
        if self.settings.get("response_style") == "hindi":
            return (
                "Aap bol sakte hain: what time is it, tell me time, add todo, show pending tasks, "
                "complete task, delete task, mark gym completed, show habits, show streak, "
                "set language hindi, set language english, set voice zira, set voice david, "
                "set voice hazel, help, exit, ya stop jarvis."
            )

        return (
            "You can say: what time is it, tell me time, add todo, show pending tasks, "
            "complete task, delete task, mark gym completed, show habits, show streak, "
            "set language hindi, set language english, set voice zira, set voice david, "
            "set voice hazel, help, exit, or stop jarvis."
        )

    def _handle_add_todo(self):
        """Ask for todo details and save the task."""
        task_name = self.listener.ask("Enter task name or press Enter to speak: ")
        task_date = self.listener.ask("Enter task date (YYYY-MM-DD) or press Enter to speak/use today: ")
        task_time = self.listener.ask("Enter task time (HH:MM) or press Enter to speak/use default 09:00: ")

        if not task_name:
            return self._message("task_name_empty")

        if not task_date:
            task_date = get_today_date()

        if not task_time:
            task_time = "09:00"

        self.todo_manager.add_task(task_name, task_date, task_time)
        return self._message("task_added")

    def _handle_show_pending_tasks(self):
        """Return a human-friendly pending task summary."""
        pending_tasks = self.todo_manager.get_pending_tasks()

        if not pending_tasks:
            return self._message("no_pending_tasks")

        task_lines = []
        for task in pending_tasks:
            task_lines.append(f"Task {task[0]}: {task[1]} on {task[2]} at {task[3]}")

        return self._pending_task_intro(len(pending_tasks)) + " " + " | ".join(task_lines)

    def _handle_complete_task(self):
        """Mark a todo as completed."""
        task_id = self.listener.ask("Enter task id to complete or press Enter to speak: ")

        if not task_id.isdigit():
            return self._message("invalid_task_id")

        updated = self.todo_manager.complete_task(int(task_id))

        if not updated:
            return self._message("task_complete_failed")

        return self._message("task_completed")

    def _handle_delete_task(self):
        """Delete a todo task."""
        task_id = self.listener.ask("Enter task id to delete or press Enter to speak: ")

        if not task_id.isdigit():
            return self._message("invalid_task_id")

        deleted = self.todo_manager.delete_task(int(task_id))

        if not deleted:
            return self._message("task_delete_failed")

        return self._message("task_deleted")

    def _handle_mark_habit(self, command):
        """Mark a habit as completed for today."""
        habit_name = command.replace("mark ", "").replace(" completed", "").strip()

        if not habit_name:
            return self._message("habit_name_empty")

        result = self.habit_tracker.mark_habit_completed(habit_name)
        return result

    def _handle_show_habits(self):
        """Return the habit completion summary."""
        habit_rows = self.habit_tracker.get_habit_summary()

        if not habit_rows:
            return self._message("no_habits")

        lines = []
        for habit_name, completed_date, streak_count in habit_rows:
            lines.append(f"{habit_name} was completed on {completed_date} with streak {streak_count}")

        return self._message("habit_summary_intro") + " " + " | ".join(lines)

    def _handle_show_streaks(self):
        """Return only streak information."""
        streaks = self.habit_tracker.get_streak_summary()

        if not streaks:
            return self._message("no_streaks")

        lines = []
        for habit_name, streak_count in streaks:
            lines.append(f"{habit_name} streak is {streak_count}")

        return self._message("streak_intro") + " " + " | ".join(lines)

    def _save_style(self, style_name):
        """Save the selected response style."""
        self.settings["response_style"] = style_name
        save_settings(self.settings)

    def _set_voice(self, voice_name):
        """Save the preferred voice name."""
        self.settings["voice_name"] = voice_name
        save_settings(self.settings)
        self.speaker.set_voice_name(voice_name)

        if self.settings.get("response_style") == "hindi":
            return f"Voice ab {voice_name} par set ho gayi hai."

        return f"Voice has been set to {voice_name}."

    def _time_message(self):
        """Return a style-based time response."""
        current_time = get_current_time_text().replace("The current time is ", "").rstrip(".")

        if self.settings.get("response_style") == "hindi":
            return f"Abhi time {current_time} hai."

        return f"The current time is {current_time}."

    def _pending_task_intro(self, count):
        """Return a style-based pending-task intro."""
        if self.settings.get("response_style") == "hindi":
            return f"Aapke {count} pending tasks hain."

        return f"You have {count} pending tasks."

    def _message(self, key):
        """Return short responses in the selected style."""
        english = {
            "empty_command": "I did not receive any command.",
            "language_hindi": "Hindi style responses are now enabled.",
            "language_english": "English style responses are now enabled.",
            "exit": "Stopping JARVIS. Have a nice day.",
            "unknown_command": "Sorry, I do not know that command yet. Please try a supported command.",
            "task_name_empty": "Task name cannot be empty.",
            "task_added": "Task added successfully.",
            "no_pending_tasks": "You have no pending tasks.",
            "invalid_task_id": "Please enter a valid numeric task id.",
            "task_complete_failed": "Task not found or already completed.",
            "task_completed": "Task marked completed successfully.",
            "task_delete_failed": "Task not found.",
            "task_deleted": "Task deleted successfully.",
            "habit_name_empty": "Habit name cannot be empty.",
            "no_habits": "No habits have been completed yet.",
            "habit_summary_intro": "Here is your habit summary.",
            "no_streaks": "No streak data is available yet.",
            "streak_intro": "Here are your current streaks.",
        }

        hindi = {
            "empty_command": "Mujhe koi command nahi mili.",
            "language_hindi": "Hindi style responses ab chalu hain.",
            "language_english": "English style responses ab chalu hain.",
            "exit": "JARVIS band ho raha hai. Aapka din shubh ho.",
            "unknown_command": "Sorry, yeh command abhi supported nahi hai. Please supported command try kijiye.",
            "task_name_empty": "Task name khali nahi ho sakta.",
            "task_added": "Task successfully add ho gaya hai.",
            "no_pending_tasks": "Aapke koi pending tasks nahi hain.",
            "invalid_task_id": "Please valid numeric task id dijiye.",
            "task_complete_failed": "Task nahi mila ya pehle hi complete ho chuka hai.",
            "task_completed": "Task successfully complete ho gaya hai.",
            "task_delete_failed": "Task nahi mila.",
            "task_deleted": "Task successfully delete ho gaya hai.",
            "habit_name_empty": "Habit name khali nahi ho sakta.",
            "no_habits": "Abhi tak koi habit complete nahi hui hai.",
            "habit_summary_intro": "Yeh aapki habit summary hai.",
            "no_streaks": "Abhi koi streak data available nahi hai.",
            "streak_intro": "Yeh aapke current streaks hain.",
        }

        if self.settings.get("response_style") == "hindi":
            return hindi[key]

        return english[key]
