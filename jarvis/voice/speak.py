"""Text-to-speech helper for JARVIS."""

import subprocess

import pyttsx3
from utils.settings_manager import load_settings, save_settings


class Speaker:
    """Reusable text-to-speech class."""

    def __init__(self):
        self.settings = load_settings()
        self.engine = None
        self.tts_available = False
        self.fallback_voice_available = False

        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", self.settings["voice_rate"])
            self.engine.setProperty("volume", 1.0)
            self._set_voice()
            self.tts_available = True
        except Exception as error:
            print(f"[JARVIS] Default text-to-speech is unavailable: {error}")
            self.fallback_voice_available = self._check_powershell_voice()
            if self.fallback_voice_available:
                print("[JARVIS] PowerShell voice fallback is available.")
            else:
                print("[JARVIS] No audio voice engine is available. JARVIS will print replies only.")

    def _set_voice(self):
        """Select a clear available voice if possible."""
        if self.engine is None:
            return

        voices = self.engine.getProperty("voices")

        if not voices:
            return

        preferred_voice = self.settings.get("voice_name", "").lower()

        for voice in voices:
            voice_name = getattr(voice, "name", "").lower()
            if preferred_voice and preferred_voice in voice_name:
                self.engine.setProperty("voice", voice.id)
                return

        for voice in voices:
            voice_name = getattr(voice, "name", "").lower()
            if "english" in voice_name or "david" in voice_name or "zira" in voice_name:
                self.engine.setProperty("voice", voice.id)
                return

        self.engine.setProperty("voice", voices[0].id)

    def speak(self, message):
        """Speak a message and print it in the terminal."""
        print(f"[JARVIS] {message}")

        if self.tts_available and self.engine is not None:
            try:
                self.engine.say(message)
                self.engine.runAndWait()
                return
            except Exception as error:
                print(f"[JARVIS] Could not play default voice response: {error}")

        if self.fallback_voice_available:
            self._speak_with_powershell(message)
            return

    @staticmethod
    def _check_powershell_voice():
        """Check whether Windows System.Speech is available."""
        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Add-Type -AssemblyName System.Speech; "
            "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "Write-Output 'ok'"
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            return "ok" in result.stdout.lower()
        except Exception:
            return False

    def _speak_with_powershell(self, message):
        """Use Windows System.Speech as a fallback voice engine."""
        safe_message = message.replace("'", " ")
        safe_voice = self.settings.get("voice_name", "Microsoft Zira Desktop").replace("'", " ")
        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Add-Type -AssemblyName System.Speech; "
            "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"try {{ $speaker.SelectVoice('{safe_voice}') }} catch {{ }}; "
            "$speaker.Rate = 0; "
            f"$speaker.Speak('{safe_message}')"
        ]

        try:
            subprocess.run(command, timeout=20, check=False)
        except Exception as error:
            print(f"[JARVIS] Could not play fallback voice response: {error}")

    def set_voice_name(self, voice_name):
        """Save the preferred voice name."""
        self.settings["voice_name"] = voice_name
        save_settings(self.settings)

        if self.engine is not None:
            self._set_voice()
