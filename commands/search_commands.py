from services import search_google, search_wikipedia, search_youtube


def handle_search_command(query):
    if "google" in query:
        search_google(query)
        return True

    if "youtube" in query:
        search_youtube(query)
        return True

    if "wikipedia" in query:
        search_wikipedia(query)
        return True

    return False
