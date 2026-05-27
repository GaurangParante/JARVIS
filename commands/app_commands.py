from services import close_app, open_app


def handle_app_command(query):
    if "open" in query or "launch" in query:
        return open_app(query)

    if "close" in query:
        return close_app(query)

    return False
