import subprocess
import sys
from pathlib import Path

from services import speak


BASE_DIR = Path(__file__).resolve().parent.parent
ALARM_TEXT_FILE = BASE_DIR / "services" / "Alarmtext.txt"
ALARM_SCRIPT = BASE_DIR / "services" / "alarm.py"


def alarm(query):
    ALARM_TEXT_FILE.write_text(query, encoding="utf-8")

    startupinfo = None
    creationflags = 0
    if sys.platform.startswith("win"):
        creationflags = subprocess.CREATE_NO_WINDOW

    subprocess.Popen(
        [sys.executable, str(ALARM_SCRIPT)],
        cwd=str(BASE_DIR),
        startupinfo=startupinfo,
        creationflags=creationflags,
    )


def extract_alarm_time(query):
    return query.split("set an alarm", 1)[1].strip()


def handle_alarm_command(query):
    if "set an alarm" in query:
        alarm_time = extract_alarm_time(query)

        if not alarm_time:
            print("Input time example :- 10 and 10 and 10")
            speak("set the time")
            alarm_time = input("Please tell the time :- ")

        alarm(alarm_time)
        speak("Done, sir")
        return True

    return False
