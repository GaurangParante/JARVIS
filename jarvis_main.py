import datetime
import sys
import time

import pyaudio
import speech_recognition as sr
import win32com.client

from GreetMe import greetMe

# ================== INITIALIZATION ==================
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 1


def speak(audio):
    # print(f"Speaking: {audio}")
    try:
        speaker.Speak(audio)
    except Exception as e:
        print("Speak Error:", e)


def get_microphone_candidates():
    bluetooth_input_keywords = ("headset", "hands-free", "hf audio", "input (@system32")
    fallback_keywords = ("realtek", "microphone", "mic input", "digital microphone")
    blocked_keywords = ("output", "speaker", "stereo mix", "mapper", "headphones", "sound mapper")
    bluetooth_candidates = []
    fallback_candidates = []
    default_candidates = []
    audio = pyaudio.PyAudio()

    try:
        for index in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(index)
            if info.get("maxInputChannels", 0) <= 0:
                continue

            name = str(info.get("name", ""))
            lowered = name.lower()

            if any(keyword in lowered for keyword in blocked_keywords):
                continue

            if any(keyword in lowered for keyword in bluetooth_input_keywords):
                bluetooth_candidates.append((index, name))
            elif any(keyword in lowered for keyword in fallback_keywords):
                fallback_candidates.append((index, name))
            else:
                default_candidates.append((index, name))
    finally:
        audio.terminate()

    return bluetooth_candidates + fallback_candidates + default_candidates + [(None, "default microphone")]


def can_open_microphone(mic_index):
    if mic_index is None:
        return True

    audio = pyaudio.PyAudio()
    stream = None

    try:
        info = audio.get_device_info_by_index(mic_index)
        channels = max(1, min(int(info.get("maxInputChannels", 1)), 1))
        sample_rate = int(info.get("defaultSampleRate", 16000))
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            input_device_index=mic_index,
            frames_per_buffer=1024,
            start=False,
        )
        return True
    except Exception:
        return False
    finally:
        if stream is not None:
            try:
                stream.close()
            except Exception:
                pass
        audio.terminate()


def listen_from_microphone(recognizer, mic_index, mic_name):
    label = mic_name if mic_index is not None else "default microphone"
    # print(f"Trying mic: {label}" + (f" (index {mic_index})" if mic_index is not None else ""))

    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening.....")
            recognizer.pause_threshold = 1
            recognizer.non_speaking_duration = 0.5
            recognizer.energy_threshold = 400
            recognizer.dynamic_energy_threshold = True
            return recognizer.listen(source, timeout=4)
    except Exception as e:
        # print(f"Mic open/listen failed for {label}: {e}")
        return None


def takeCommand():
    r = sr.Recognizer()
    audio = None

    for mic_index, mic_name in get_microphone_candidates():
        if not can_open_microphone(mic_index):
            continue

        lowered_name = mic_name.lower()
        if "headset" in lowered_name or "hands-free" in lowered_name or "hf audio" in lowered_name or "input (@" in lowered_name:
            # print(f"Using Bluetooth mic: {mic_name}" + (f" (index {mic_index})" if mic_index is not None else ""))
            pass
        elif mic_index is not None:
            # print(f"Using laptop mic: {mic_name} (index {mic_index})")
            pass
        else:
            # print("Using default microphone")
            pass

        audio = listen_from_microphone(r, mic_index, mic_name)
        if audio is not None:
            break

    if audio is None:
        return "None"

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}\n")
        return query.lower()
    except Exception:
        return "None"


def should_exit(query):
    return (
        "exit" in query
        or "stop jarvis" in query
        or "close jarvis" in query
        or "shutdown jarvis" in query
    )


# ================== MAIN LOOP ==================
if __name__ == "__main__":
    print("Assistant is ready. Say 'wake up' or 'jarvis' to start.\n")

    try:
        while True:
            query = takeCommand()

            if query == "None":
                continue

            if should_exit(query):
                speak("Shutting down. Goodbye sir.")
                print("Assistant closed.")
                sys.exit(0)

            if "wake up" in query or "jarvis" in query:
                greetMe(speak)
                # time.sleep(0.5)
                # speak("I'm now active sir.")
                # print("Active Mode ON. Say 'go to sleep' or 'exit' to stop.\n")

                while True:
                    query = takeCommand()

                    if query == "None":
                        continue

                    if should_exit(query):
                        speak("Shutting down. Goodbye sir.")
                        print("Assistant closed.")
                        sys.exit(0)

                    if "go to sleep" in query or "sleep" in query:
                        speak("Ok sir, going to sleep. Call me anytime.")
                        print("Assistant went to sleep.\n")
                        break

                    if "hear me" in query:
                        speak("Yes sir")

                    elif "how are you" in query or "how r u" in query:
                        speak("I'm doing great sir, thank you!")

                    elif "who are you" in query:
                        speak("I'm Jarvis, your personal assistant.")

                    elif "time" in query:
                        time_now = datetime.datetime.now().strftime("%H:%M")
                        speak(f"The current time is {time_now}")

                    elif "hello" in query or "hi" in query:
                        speak("Hello sir, how can I help you?")

                    elif "google" in query:
                        from SearchNow import searchGoogle
                        searchGoogle(query)

                    elif "youtube" in query:
                        from SearchNow import searchYoutube
                        searchYoutube(query)

                    elif "wikipedia" in query:
                        from SearchNow import searchWikipedia
                        searchWikipedia(query)

                    else:
                        speak("Sorry sir, I didn't catch that.")
    except KeyboardInterrupt:
        print("\nAssistant stopped from keyboard.")
        try:
            speaker.Speak("")
        except Exception:
            pass
