"""Simple settings helper for JARVIS."""

import json
from pathlib import Path


SETTINGS_FILE = Path(__file__).resolve().parents[1] / "data" / "settings.json"

DEFAULT_SETTINGS = {
    "voice_name": "Microsoft Zira Desktop",
    "voice_rate": 170,
    "response_style": "english",
}


def load_settings():
    """Load settings from file or return defaults."""
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        stored_settings = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    settings = DEFAULT_SETTINGS.copy()
    settings.update(stored_settings)
    return settings


def save_settings(settings):
    """Save settings to disk."""
    SETTINGS_FILE.write_text(json.dumps(settings, indent=4), encoding="utf-8")
