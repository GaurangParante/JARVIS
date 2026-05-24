# JARVIS - Personal AI Desktop Assistant

JARVIS is a beginner-friendly Python desktop assistant project. It uses voice input, voice replies, SQLite storage, and simple modular code so you can learn from it and extend it later.

## Features

- Voice input using your microphone
- Voice replies using offline text-to-speech
- Typed command input and voice command input in the same session
- Time commands
- Todo management
- Habit tracking with streak support
- SQLite database created automatically
- Colored terminal output
- Greeting message
- Today's pending task summary
- Command logging in the terminal
- Safe fallback to typed input if voice recognition is unavailable
- Command log saved to `data/command_log.txt`
- Startup greeting voice
- Hindi or English style responses

## Project Structure

```text
jarvis/
│
├── main.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── db.py
│   └── jarvis.db
│
├── voice/
│   ├── listen.py
│   └── speak.py
│
├── assistant/
│   ├── commands.py
│   └── brain.py
│
├── todo/
│   └── todo_manager.py
│
├── habits/
│   └── habit_tracker.py
│
├── utils/
│   └── time_utils.py
│
└── data/
    └── habits.json
```

## Requirements

- Python 3.12 or later
- Microphone for voice commands
- Speaker or headphones for voice replies

## Installation

### 1. Open terminal in the project folder

Move to the project directory:

```powershell
cd d:\gaurang\JARVIS\jarvis
```

### 2. Create a virtual environment (recommended)

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## Important Voice Setup

### Microphone note

JARVIS now supports two microphone modes:

1. `speech_recognition` microphone mode when PyAudio is available
2. `sounddevice` fallback microphone mode when PyAudio is missing

This means the project can still use the microphone even on systems where `PyAudio` fails to install.

### Speech recognition note

This project uses `speech_recognition` with Google speech recognition for easy setup. That means:

- Microphone capture is local
- Text-to-speech is local
- Database is local
- If online speech recognition fails, JARVIS falls back to typed input so the app still runs

Later, you can replace the recognizer with a fully offline engine if you want.

## How to Run

From the `jarvis` folder:

```powershell
python main.py
```

## Session Flow

1. Run `python main.py`
2. Type `wake jarvis` once
3. After that, JARVIS stays active
4. For each next step:
   - Type a command and press Enter
   - Or just press Enter and speak your command
5. JARVIS keeps running until you say or type `exit`

## Example Commands

### Time

- `what time is it`
- `tell me time`

### Todo

- `add todo`
- `show pending tasks`
- `complete task`
- `delete task`

When JARVIS asks follow-up questions, you can answer by typing or by voice.

### Habits

- `mark gym completed`
- `show habits`
- `show streak`

### Exit

- `exit`
- `stop jarvis`

### Help

- `help`
- `show commands`
- `what can you do`

### Voice and Style

- `set voice zira`
- `set voice david`
- `set voice hazel`
- `set language hindi`
- `set language english`

## How It Works

1. `main.py` starts JARVIS
2. Database tables are created automatically
3. JARVIS greets you and shows today's pending tasks
4. You type `wake jarvis` one time to begin the session
5. JARVIS waits for typed or spoken commands
6. Speech is converted to text when needed
7. Command processor decides what to do
8. JARVIS performs the action
9. JARVIS speaks the response and waits for the next command

## Troubleshooting

### Microphone is not working

- Check that your microphone is connected
- Check Windows privacy settings for microphone access
- If PyAudio is unavailable, JARVIS will automatically try `sounddevice`
- If microphone capture still fails, typed fallback will still work

### JARVIS says it could not understand audio

- Speak clearly
- Reduce background noise
- Wait for the `Listening...` message before speaking
- Try the command again

### Voice is not speaking

- Check speaker volume
- Make sure `pyttsx3` is installed
- Close other apps that may be controlling the audio device

### Database file is missing

The database is created automatically on first run. If needed, just run:

```powershell
python main.py
```

### Commands are not recognized

Use the simple command phrases listed above. This project is intentionally beginner-friendly, so command parsing is based on easy keyword matching.

## Where to Find Your Commands

- Supported command handling is in [assistant/commands.py](d:\gaurang\JARVIS\jarvis\assistant\commands.py)
- Command examples are listed in this `README.md`
- Every command you use is saved to `data/command_log.txt`
- Voice and style settings are saved in `data/settings.json`

## Files Overview

- `main.py`: starts the program
- `database/db.py`: handles SQLite setup and queries
- `voice/listen.py`: captures microphone or typed input
- `voice/speak.py`: text-to-speech replies
- `assistant/commands.py`: command routing
- `assistant/brain.py`: main assistant loop
- `todo/todo_manager.py`: todo features
- `habits/habit_tracker.py`: habit features and streaks
- `utils/time_utils.py`: time helper functions
- `data/habits.json`: stores default habits list

## Default Habits

The project loads default habits from `data/habits.json`. You can edit that file and add your own habits.

## Future Improvements

- Wake word support
- Fully offline speech-to-text
- Better natural language understanding
- GUI version
- Notifications and reminders

## License

This project is for learning and personal use.
