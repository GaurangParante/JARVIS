# JARVIS

Voice assistant project in Python with a cleaner module structure for commands and shared services.

## Project Structure

```text
JARVIS/
  jarvis_main.py
  commands_cheatsheet.txt
  developer_reference.md
  future_ideas.txt
  commands/
    __init__.py
    app_commands.py
    basic_commands.py
    search_commands.py
    weather_commands.py
  services/
    __init__.py
    app_service.py
    greeting.py
    listener.py
    search_service.py
    speech.py
    weather_service.py
```

## How It Is Organized

- `jarvis_main.py` handles startup, wake/sleep flow, and command routing.
- `commands/` contains user-facing handlers for basic replies, app actions, search, and weather.
- `services/` contains reusable helpers for speech, microphone input, app control, search, greeting, and weather.
- `services/__init__.py` is the shared import surface for common helpers.
- `commands_cheatsheet.txt` lists the currently supported voice commands.
- `developer_reference.md` explains which function is in which module and why it is used.
- `future_ideas.txt` tracks commands and features to add later.

## Current Supported Commands

- Wake: `wake up`, `jarvis`
- Sleep: `go to sleep`, `sleep`
- Exit: `exit`, `stop jarvis`, `close jarvis`, `shutdown jarvis`
- Basic: `hear me`, `hello`, `hi`, `how are you`, `who are you`, `about you`, `time`
- Search: Google, YouTube, and Wikipedia queries
- Weather: `weather`, `temperature`
- App control: open and close supported desktop apps and websites

For examples, check `commands_cheatsheet.txt`.

## Why This Structure

- Keeps the main file short and easier to read.
- Makes each command easier to change without touching unrelated logic.
- Reduces the chance of one feature making the whole assistant messy.
- Gives you one clean shared place for common services without turning the project into one giant import file.

## Git Notes

The `.gitignore` already excludes common local noise such as:

- virtual environments
- cache folders
- editor settings
- local environment files
- temp and log files
