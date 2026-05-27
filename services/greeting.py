import datetime

from .speech import speak


def greet_user():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        greeting = "Good Morning, sir."
    elif 12 <= hour < 18:
        greeting = "Good Afternoon, sir."
    else:
        greeting = "Good Evening, sir."

    speak(greeting)
