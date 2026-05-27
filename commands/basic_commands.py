import datetime

from services import speak


def handle_basic_command(query):
    if "hear me" in query:
        speak("Yes sir")
        return True

    if "how are you" in query or "how r u" in query:
        speak("I'm doing great sir, thank you!")
        return True

    if "who are you" in query or "about you" in query:
        speak("I'm Jarvis, your personal assistant.")
        return True

    if "time" in query:
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {time_now}")
        return True

    if "hello" in query or "hi" in query:
        speak("Hello sir, how can I help you?")
        return True

    return False
