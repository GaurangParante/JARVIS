import datetime


def greetMe(speak):
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        greeting = "Good Morning, sir."
    elif 12 <= hour < 18:
        greeting = "Good Afternoon, sir."
    else:
        greeting = "Good Evening, sir."

    speak(f"{greeting}")
