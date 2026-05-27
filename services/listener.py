import pyaudio
import speech_recognition as sr


LISTEN_TIMEOUT_SECONDS = 6
PHRASE_TIME_LIMIT_SECONDS = 8
AMBIENT_NOISE_ADJUST_SECONDS = 0.8
BASE_ENERGY_THRESHOLD = 250


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


def listen_from_microphone(recognizer, mic_index):
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening.....")
            recognizer.pause_threshold = 1.2
            recognizer.non_speaking_duration = 0.5
            recognizer.operation_timeout = LISTEN_TIMEOUT_SECONDS
            recognizer.energy_threshold = BASE_ENERGY_THRESHOLD
            recognizer.dynamic_energy_threshold = True
            recognizer.dynamic_energy_adjustment_damping = 0.15
            recognizer.dynamic_energy_ratio = 1.5
            recognizer.adjust_for_ambient_noise(source, duration=AMBIENT_NOISE_ADJUST_SECONDS)
            recognizer.energy_threshold = min(recognizer.energy_threshold, BASE_ENERGY_THRESHOLD)
            return recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT_SECONDS,
                phrase_time_limit=PHRASE_TIME_LIMIT_SECONDS,
            )
    except Exception:
        return None


def take_command():
    recognizer = sr.Recognizer()
    audio = None

    for mic_index, mic_name in get_microphone_candidates():
        if not can_open_microphone(mic_index):
            continue

        lowered_name = mic_name.lower()
        if "headset" in lowered_name or "hands-free" in lowered_name or "hf audio" in lowered_name or "input (@" in lowered_name:
            pass
        elif mic_index is not None:
            pass
        else:
            pass

        audio = listen_from_microphone(recognizer, mic_index)
        if audio is not None:
            break

    if audio is None:
        return "None"

    try:
        print("Understanding...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"You said: {query}\n")
        return query.lower()
    except Exception:
        return "None"
