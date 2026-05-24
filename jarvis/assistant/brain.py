"""Main assistant brain that connects all modules together."""

from pathlib import Path
from colorama import Fore, Style, init

from assistant.commands import CommandProcessor
from habits.habit_tracker import HabitTracker
from todo.todo_manager import TodoManager
from utils.settings_manager import load_settings
from voice.listen import VoiceListener
from voice.speak import Speaker


class JarvisBrain:
    """Run the assistant loop."""

    def __init__(self):
        init(autoreset=True)
        self.log_file = Path(__file__).resolve().parents[1] / "data" / "command_log.txt"
        self.settings = load_settings()

        self.listener = VoiceListener()
        self.speaker = Speaker()
        self.todo_manager = TodoManager()
        self.habit_tracker = HabitTracker()
        self.command_processor = CommandProcessor(
            todo_manager=self.todo_manager,
            habit_tracker=self.habit_tracker,
            listener=self.listener,
            speaker=self.speaker,
        )

    def run(self):
        """Start the JARVIS loop."""
        self._show_greeting()

        while True:
            wake_command = input(
                Fore.CYAN + "Type 'wake jarvis' to start listening or 'exit' to quit: " + Style.RESET_ALL
            ).strip().lower()

            if wake_command == "exit":
                self.speaker.speak("Stopping JARVIS. Goodbye.")
                break

            if wake_command != "wake jarvis":
                print(Fore.YELLOW + "[JARVIS] Please type 'wake jarvis' to continue.")
                continue

            self.speaker.speak("Session started. Type a command or press Enter to speak. Say exit to close JARVIS.")
            self._run_active_session()

            # If the session loop exits because the user said exit, stop the app.
            break

    def _run_active_session(self):
        """Keep JARVIS active until the user exits."""
        while True:
            command = self.listener.ask(
                Fore.CYAN + "Type a command, or press Enter to use voice: " + Style.RESET_ALL
            )

            self._log_command(command)
            result = self.command_processor.process(command)
            self.speaker.speak(result["message"])

            if result["exit"]:
                return

    def _show_greeting(self):
        """Display a greeting and today's task summary."""
        summary_count = self.todo_manager.get_today_pending_count()

        print(Fore.GREEN + "=" * 55)
        print(Fore.GREEN + "JARVIS Desktop Assistant Started")
        print(Fore.GREEN + "=" * 55)
        print(Fore.BLUE + f"[JARVIS] Welcome back. You have {summary_count} pending task(s) for today.")
        print(Fore.BLUE + "[JARVIS] Supported commands: time, todos, habits, exit.")
        print(Fore.BLUE + "[JARVIS] Type or say 'help' to hear all supported commands.")
        print(Fore.BLUE + "[JARVIS] After waking once, the session stays active until you say exit.")

        self.speaker.speak(self._startup_greeting(summary_count))

    def _log_command(self, command):
        """Print a simple command log line."""
        print(Fore.MAGENTA + f"[LOG] Command received: {command}")
        with self.log_file.open("a", encoding="utf-8") as log_file:
            log_file.write(command + "\n")

    def _startup_greeting(self, summary_count):
        """Return a style-based startup greeting."""
        self.settings = load_settings()

        if self.settings.get("response_style") == "hindi":
            return (
                f"Namaste. JARVIS tayyar hai. Aaj ke liye aapke {summary_count} pending tasks hain. "
                "Aap type bhi kar sakte hain aur bol bhi sakte hain."
            )

        return (
            f"Hello. JARVIS is ready. You have {summary_count} pending tasks for today. "
            "You can type commands or speak them."
        )
