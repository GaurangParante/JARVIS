import sys

from commands import handle_active_command
from services import clear_speech, greet_user, speak, take_command


def should_exit(query):
    return (
        "exit" in query
        or "stop jarvis" in query
        or "close jarvis" in query
        or "shutdown jarvis" in query
    )


def should_wake(query):
    return "wake up" in query or "jarvis" in query


def run_active_mode():
    while True:
        query = take_command()

        if query == "None":
            continue

        if should_exit(query):
            speak("Shutting down. Goodbye sir.")
            print("Assistant closed.")
            sys.exit(0)

        if "go to sleep" in query or "sleep" in query:
            speak("Ok sir, going to sleep. Call me anytime.")
            print("Assistant went to sleep.\n")
            return

        if not handle_active_command(query):
            speak("Sorry sir, I didn't catch that.")


def main():
    print("Assistant is ready. Say 'wake up' or 'jarvis' to start.\n")

    try:
        while True:
            query = take_command()

            if query == "None":
                continue

            if should_exit(query):
                speak("Shutting down. Goodbye sir.")
                print("Assistant closed.")
                sys.exit(0)

            if should_wake(query):
                greet_user()
                run_active_mode()
    except KeyboardInterrupt:
        print("\nAssistant stopped from keyboard.")
        clear_speech()


if __name__ == "__main__":
    main()
