from .basic_commands import handle_basic_command
from .search_commands import handle_search_command
from .weather_commands import handle_weather_command
from .app_commands import handle_app_command
from .alarm_commands import handle_alarm_command


def handle_active_command(query):
    handlers = (
        handle_basic_command,
        handle_alarm_command,
        handle_app_command,
        handle_search_command,
        handle_weather_command,
    )

    for handler in handlers:
        if handler(query):
            return True

    return False
