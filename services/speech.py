import win32com.client


speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 1


def speak(audio):
    try:
        speaker.Speak(audio)
    except Exception as error:
        print("Speak Error:", error)


def clear_speech():
    try:
        speaker.Speak("")
    except Exception:
        pass
