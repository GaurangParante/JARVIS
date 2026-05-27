# JARVIS Developer Reference

This file is for you as the developer so you can quickly understand:

- which module contains which function
- where that function is used
- why that function exists

## Main Flow

### `jarvis_main.py`

- `should_exit(query)`
  Why used: checks common exit phrases like `exit` and `stop jarvis` so shutdown logic stays in one place.

- `should_wake(query)`
  Why used: checks wake words like `wake up` and `jarvis` before assistant enters active mode.

- `run_active_mode()`
  Why used: keeps Jarvis listening after wake-up and sends each recognized query to the command router.

- `main()`
  Why used: app entry point. Starts passive listening, wakes Jarvis, and handles keyboard interrupt cleanup.

## Command Router

### `commands/__init__.py`

- `handle_active_command(query)`
  Why used: central router for active mode. It sends the same query to each command module one by one.
  Used by: `jarvis_main.py`

## Command Modules

### `commands/basic_commands.py`

- `handle_basic_command(query)`
  Why used: handles simple conversational commands like `hello`, `time`, and `who are you`.
  Uses: `services.speak`
  Called by: `commands.handle_active_command`

### `commands/app_commands.py`

- `handle_app_command(query)`
  Why used: decides whether the user wants to open or close an app, website, or tab.
  Uses: `services.open_app`, `services.close_app`
  Called by: `commands.handle_active_command`

### `commands/search_commands.py`

- `handle_search_command(query)`
  Why used: routes search-related voice commands to Google, YouTube, or Wikipedia helpers.
  Uses: `services.search_google`, `services.search_youtube`, `services.search_wikipedia`
  Called by: `commands.handle_active_command`

### `commands/weather_commands.py`

- `handle_weather_command(query)`
  Why used: handles `weather` and `temperature` commands and speaks the response.
  Uses: `services.fetch_weather`, `services.fetch_temperature`, `services.speak`
  Called by: `commands.handle_active_command`

## Shared Service Export Layer

### `services/__init__.py`

- `speak`
- `clear_speech`
- `take_command`
- `greet_user`
- `open_app`
- `close_app`
- `search_google`
- `search_youtube`
- `search_wikipedia`
- `fetch_temperature`
- `fetch_weather`

Why used: gives one common import surface so command files can do `from services import ...` instead of importing from many service files directly.

## Service Modules

### `services/speech.py`

- `speaker`
  Why used: shared Windows SAPI voice object so the whole app speaks with one configured voice instance.

- `speak(audio)`
  Why used: speaks text aloud everywhere in the project.
  Used by: greeting, basic commands, search service, weather commands, app service, main shutdown/sleep messages.

- `clear_speech()`
  Why used: clears or safely stops speech during shutdown/interrupt.
  Used by: `jarvis_main.py`

### `services/greeting.py`

- `greet_user()`
  Why used: gives time-based greeting after wake-up.
  Uses: `services.speech.speak`
  Used by: `jarvis_main.py`

### `services/listener.py`

- `get_microphone_candidates()`
  Why used: finds possible microphones and prefers Bluetooth or real microphone inputs over bad devices.

- `can_open_microphone(mic_index)`
  Why used: checks whether a microphone device can actually be opened before trying to listen from it.

- `listen_from_microphone(recognizer, mic_index)`
  Why used: records audio from the selected microphone with timeout and ambient noise adjustment.

- `take_command()`
  Why used: main speech-to-text function. It listens, converts speech to text, and returns lowercase user query.
  Used by: `jarvis_main.py`

### `services/search_service.py`

- `clean_query(query, keyword)`
  Why used: removes filler words so search text becomes cleaner.

- `search_google(query)`
  Why used: opens a Google search and tries to speak a short summary.

- `search_youtube(query)`
  Why used: opens YouTube search results and plays the matching video/search.

- `search_wikipedia(query)`
  Why used: fetches and speaks a Wikipedia summary for knowledge-type questions.

Used by: `commands/search_commands.py`

### `services/weather_service.py`

- `fetch_temperature(city)`
  Why used: gets the current temperature from `wttr.in`.

- `fetch_weather(city)`
  Why used: gets weather condition plus temperature from `wttr.in`.

Used by: `commands/weather_commands.py`

### `services/app_service.py`

- `APP_MAP`
  Why used: stores supported desktop app names, aliases, launch targets, and process names in one place.

- `WEB_APP_MAP`
  Why used: stores supported website aliases and URLs in one place.

- `_expand_path(raw_path)`
  Why used: resolves Windows environment variables inside configured app paths.

- `_match_app(query)`
  Why used: finds which desktop app the user is talking about.

- `_match_web_app(query)`
  Why used: finds which website/web app the user is talking about.

- `_existing_path(app_info)`
  Why used: checks whether a configured app path actually exists on the system.

- `_launch_target(app_info)`
  Why used: decides the best way to launch an app, such as URI, explicit file path, or executable name.

- `_open_with_target(target)`
  Why used: opens a Windows settings URI, absolute executable path, or command.

- `_close_current_tab(tab_name=None)`
  Why used: closes the browser tab using `Ctrl + W`.

- `open_app(query)`
  Why used: opens desktop apps, supported websites, or direct `.com` style sites from voice command.
  Used by: `commands/app_commands.py`

- `close_app(query)`
  Why used: closes matching desktop apps or browser tabs from voice command.
  Used by: `commands/app_commands.py`

## Quick Dependency Map

- `jarvis_main.py` -> `commands`, `services`
- `commands/*` -> `services`
- `services/greeting.py` -> `services/speech.py`
- `services/search_service.py` -> browser/search libraries + `services/speech.py`
- `services/weather_service.py` -> `requests`
- `services/app_service.py` -> `pyautogui`, `subprocess`, `webbrowser`
- `services/listener.py` -> `pyaudio`, `speech_recognition`

## Suggested Rule For Future Work

When adding a new feature:

1. Put user intent detection inside a file in `commands/`
2. Put reusable action logic inside a file in `services/`
3. If many modules need the same helper, export it from `services/__init__.py`
4. Update `commands_cheatsheet.txt` if the user can speak that command
5. Update `future_ideas.txt` or `README.md` if the feature changes project docs
