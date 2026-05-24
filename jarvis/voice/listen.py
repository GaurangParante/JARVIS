"""Voice input helper for microphone and terminal fallback."""

import speech_recognition as sr
import sounddevice as sd


class VoiceListener:
    """Handle microphone listening and typed fallback."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 300

    def listen(self):
        """
        Listen for a command.

        Returns:
            str: Recognized command text in lowercase.
        """
        try:
            audio = self._record_audio()
        except Exception as error:
            print(f"[JARVIS] Microphone error: {error}")
            return self._typed_fallback("Type your command instead: ")

        try:
            print("[JARVIS] Recognizing...")
            command = self.recognizer.recognize_google(audio)
            command = command.lower().strip()
            print(f"[YOU] {command}")
            return command
        except sr.UnknownValueError:
            print("[JARVIS] I could not understand the audio.")
            return self._typed_fallback("Type your command instead: ")
        except sr.RequestError as error:
            print(f"[JARVIS] Speech service error: {error}")
            return self._typed_fallback("Type your command instead: ")
        except Exception as error:
            print(f"[JARVIS] Unexpected listening error: {error}")
            return self._typed_fallback("Type your command instead: ")

    def ask_text(self, prompt):
        """Ask the user a follow-up question using typed input."""
        return self._typed_fallback(prompt)

    def ask(self, prompt):
        """
        Ask the user for input in two ways.

        If the user types text, that text is used.
        If the user presses Enter without typing, JARVIS listens by microphone.
        """
        typed_value = input(prompt).strip().lower()

        if typed_value:
            return typed_value

        print("[JARVIS] No typed input detected. Switching to voice input.")
        return self.listen()

    def _record_audio(self):
        """Record audio using PyAudio first, then sounddevice as fallback."""
        try:
            return self._record_with_speech_recognition_mic()
        except Exception as microphone_error:
            print(f"[JARVIS] Default microphone mode unavailable: {microphone_error}")
            print("[JARVIS] Switching to sounddevice microphone mode.")
            return self._record_with_sounddevice()

    def _record_with_speech_recognition_mic(self):
        """Record audio with speech_recognition's Microphone class."""
        with sr.Microphone() as source:
            print("[JARVIS] Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            return self.recognizer.listen(source, timeout=5, phrase_time_limit=8)

    @staticmethod
    def _record_with_sounddevice():
        """
        Record audio without PyAudio.

        This fallback records a short audio clip directly from the default
        input device and converts it into SpeechRecognition audio data.
        """
        sample_rate = 16000
        duration_seconds = 6

        print(f"[JARVIS] Listening with fallback microphone for {duration_seconds} seconds...")
        recording = sd.rec(
            int(duration_seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
        )
        sd.wait()

        audio_bytes = recording.tobytes()
        return sr.AudioData(audio_bytes, sample_rate, 2)

    @staticmethod
    def _typed_fallback(prompt):
        """Use keyboard input when voice is unavailable."""
        return input(prompt).strip().lower()
