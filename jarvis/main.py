"""Main entry point for the JARVIS desktop assistant project."""

from database.db import initialize_database
from assistant.brain import JarvisBrain


def main():
    """Start the assistant."""
    initialize_database()

    brain = JarvisBrain()
    brain.run()


if __name__ == "__main__":
    main()
