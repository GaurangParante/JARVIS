import os
import subprocess
import webbrowser
import pyautogui
from pathlib import Path

from .speech import speak


APP_MAP = {
    "command prompt": {
        "aliases": ("command prompt", "cmd", "terminal"),
        "launch": ("cmd.exe",),
        "processes": ("cmd.exe",),
    },
    "paint": {
        "aliases": ("paint", "mspaint"),
        "launch": ("mspaint.exe",),
        "processes": ("mspaint.exe",),
    },
    "word": {
        "aliases": ("word", "ms word", "microsoft word"),
        "launch": ("winword.exe",),
        "processes": ("winword.exe",),
    },
    "excel": {
        "aliases": ("excel", "ms excel", "microsoft excel"),
        "launch": ("excel.exe",),
        "processes": ("excel.exe",),
    },
    "powerpoint": {
        "aliases": ("powerpoint", "power point", "ppt"),
        "launch": ("powerpnt.exe",),
        "processes": ("powerpnt.exe",),
    },
    "chrome": {
        "aliases": ("chrome", "google chrome", "browser"),
        "launch": ("chrome.exe",),
        "processes": ("chrome.exe",),
    },
    "vscode": {
        "aliases": ("vscode", "vs code", "visual studio code"),
        "launch": ("code.exe",),
        "processes": ("code.exe",),
    },
    "notepad": {
        "aliases": ("notepad",),
        "launch": ("notepad.exe",),
        "processes": ("notepad.exe",),
    },
    "calculator": {
        "aliases": ("calculator", "calc"),
        "launch": ("calc.exe",),
        "processes": ("CalculatorApp.exe", "calc.exe"),
    },
    "settings": {
        "aliases": ("settings", "windows settings"),
        "uri": "ms-settings:",
        "processes": ("SystemSettings.exe",),
    },
    "heidisql": {
        "aliases": ("heidisql", "heidi sql","heidi","sql"),
        "launch": ("heidisql.exe",),
        "paths": (
            r"C:\Program Files\HeidiSQL\heidisql.exe",
            r"C:\Program Files (x86)\HeidiSQL\heidisql.exe",
        ),
        "processes": ("heidisql.exe",),
    },
    "sourcetree": {
        "aliases": ("sourcetree", "source tree"),
        "launch": ("SourceTree.exe",),
        "paths": (
            r"C:\Program Files\Atlassian\SourceTree\SourceTree.exe",
            r"C:\Program Files (x86)\Atlassian\SourceTree\SourceTree.exe",
            r"%LOCALAPPDATA%\SourceTree\SourceTree.exe",
        ),
        "processes": ("SourceTree.exe",),
    },
    "github desktop": {
        "aliases": ("github desktop", "github", "gihub desktop", "git hub desktop"),
        "launch": ("GitHubDesktop.exe",),
        "paths": (
            r"%LOCALAPPDATA%\GitHubDesktop\GitHubDesktop.exe",
        ),
        "processes": ("GitHubDesktop.exe",),
    },
    "postman": {
        "aliases": ("postman",),
        "launch": ("Postman.exe",),
        "paths": (
            r"%LOCALAPPDATA%\Postman\Postman.exe",
            r"C:\Program Files\Postman\Postman.exe",
            r"C:\Program Files (x86)\Postman\Postman.exe",
        ),
        "processes": ("Postman.exe",),
    },
}

WEB_APP_MAP = {
    "google": {
        "aliases": ("google",),
        "url": "https://www.google.com",
    },
    "youtube": {
        "aliases": ("youtube", "yt"),
        "url": "https://www.youtube.com",
    },
    "instagram": {
        "aliases": ("instagram", "insta"),
        "url": "https://www.instagram.com",
    },
    "facebook": {
        "aliases": ("facebook", "fb"),
        "url": "https://www.facebook.com",
    },
    "linkedin": {
        "aliases": ("linkedin", "linked in"),
        "url": "https://www.linkedin.com",
    },
    "github": {
        "aliases": ("github website", "github site"),
        "url": "https://www.github.com",
    },
    "gmail": {
        "aliases": ("gmail", "mail"),
        "url": "https://mail.google.com",
    },
}


def _expand_path(raw_path):
    return os.path.expandvars(raw_path)


def _match_app(query):
    lowered_query = query.lower()
    for app_name, app_info in APP_MAP.items():
        if any(alias in lowered_query for alias in app_info["aliases"]):
            return app_name, app_info
    return None, None


def _match_web_app(query):
    lowered_query = query.lower()
    for web_app_name, web_app_info in WEB_APP_MAP.items():
        if any(alias in lowered_query for alias in web_app_info["aliases"]):
            return web_app_name, web_app_info
    return None, None


def _existing_path(app_info):
    for raw_path in app_info.get("paths", ()):
        expanded_path = _expand_path(raw_path)
        if Path(expanded_path).exists():
            return expanded_path
    return None


def _launch_target(app_info):
    uri = app_info.get("uri")
    if uri:
        return uri

    existing_path = _existing_path(app_info)
    if existing_path:
        return existing_path

    launch_targets = app_info.get("launch", ())
    return launch_targets[0] if launch_targets else None


def _open_with_target(target):
    if target.startswith("ms-settings:"):
        subprocess.Popen(["cmd", "/c", "start", "", target], shell=False)
        return True

    if os.path.isabs(target) and Path(target).exists():
        os.startfile(target)
        return True

    subprocess.Popen([target], shell=False)
    return True


def _close_current_tab(tab_name=None):
    pyautogui.hotkey("ctrl", "w")
    if tab_name:
        speak(f"Closing {tab_name} tab, sir")
    else:
        speak("Tab closed")
    return True


def open_app(query):
    if ".com" in query or ".co.in" in query or ".org" in query:
        cleaned_query = (
            query.replace("open", "")
            .replace("jarvis", "")
            .replace("launch", "")
            .replace(" ", "")
        )
        webbrowser.open(f"https://www.{cleaned_query}")
        speak("Launching, sir")
        return True

    web_app_name, web_app_info = _match_web_app(query)
    if web_app_info:
        webbrowser.open(web_app_info["url"])
        speak(f"Opening {web_app_name}, sir")
        return True

    app_name, app_info = _match_app(query)
    if not app_info:
        return False

    target = _launch_target(app_info)
    if not target:
        speak(f"I could not find {app_name} on this system.")
        return True

    try:
        _open_with_target(target)
        speak(f"Opening {app_name}, sir")
    except Exception as error:
        print("Open App Error:", error)
        speak(f"I could not open {app_name} right now.")
    return True


def close_app(query):
    web_app_name, web_app_info = _match_web_app(query)
    if "tab" in query:
        tab_name = web_app_name if web_app_info else None
        return _close_current_tab(tab_name)

    if web_app_info and "close" in query:
        return _close_current_tab(web_app_name)

    app_name, app_info = _match_app(query)
    if not app_info:
        return False

    closed_any = False
    for process_name in app_info.get("processes", ()):
        result = subprocess.run(
            ["taskkill", "/F", "/IM", process_name],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            closed_any = True

    if closed_any:
        speak(f"Closing {app_name}, sir")
    else:
        speak(f"{app_name} is not running right now.")
    return True
