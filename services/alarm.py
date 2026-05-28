import datetime
import os
import time as time_module
from pathlib import Path

try:
    from .speech import speak
except ImportError:
    from speech import speak

BASE_DIR = Path(__file__).resolve().parent
ALARM_TEXT_FILE = BASE_DIR / "Alarmtext.txt"
MUSIC_FILE = BASE_DIR / "music.mp3"


def normalize_alarm_time(alarm_time):
    timeset = str(alarm_time).lower()
    timenow = timeset.replace(" and ", ":")
    timenow = timenow.replace("jarvis", "")
    timenow = timenow.replace("set", "")
    timenow = timenow.replace("alarm", "")
    timenow = timenow.replace(" an ", " ")
    return timenow.strip()


def play_alarm_sound():
    if MUSIC_FILE.exists():
        os.startfile(str(MUSIC_FILE))
        return

    try:
        import winsound

        winsound.Beep(1000, 1000)
    except Exception:
        print("Alarm sound file not found.")


def ring(alarm_time):
    alarm_time = normalize_alarm_time(alarm_time)
    print(alarm_time)

    while True:
        currenttime = datetime.datetime.now().strftime("%H:%M:%S")
        if currenttime == alarm_time:
            speak("Alarm Ringing, Sir")
            play_alarm_sound()
            break

        time_module.sleep(1)


def run_saved_alarm():
    alarm_time = ALARM_TEXT_FILE.read_text(encoding="utf-8")
    ALARM_TEXT_FILE.write_text("", encoding="utf-8")

    if alarm_time.strip():
        ring(alarm_time)


if __name__ == "__main__":
    run_saved_alarm()
