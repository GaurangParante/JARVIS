from services import fetch_temperature, fetch_weather, speak


DEFAULT_CITY = "Ahmedabad"


def handle_weather_command(query):
    if "temperature" in query:
        temp = fetch_temperature(DEFAULT_CITY)
        if temp:
            speak(f"Current temperature in {DEFAULT_CITY} is {temp}")
        else:
            speak("I could not fetch the temperature right now.")
        return True

    if "weather" in query:
        weather = fetch_weather(DEFAULT_CITY)
        if weather:
            speak(f"Current weather in {DEFAULT_CITY} is {weather}")
        else:
            speak("I could not fetch the weather right now.")
        return True

    return False
