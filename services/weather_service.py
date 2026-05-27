import requests


def fetch_temperature(city):
    try:
        response = requests.get(
            f"https://wttr.in/{city}",
            params={"format": "%t"},
            timeout=10,
        )
        response.raise_for_status()
        return response.text.strip() or None
    except requests.RequestException:
        return None


def fetch_weather(city):
    try:
        response = requests.get(
            f"https://wttr.in/{city}",
            params={"format": "%C, %t"},
            timeout=10,
        )
        response.raise_for_status()
        return response.text.strip() or None
    except requests.RequestException:
        return None
