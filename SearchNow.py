import webbrowser

import pywhatkit
import wikipedia
import win32com.client


speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 1


def speak(audio):
    # print(f"Speaking: {audio}")
    try:
        speaker.Speak(audio)
    except Exception as e:
        print("Speak Error:", e)


def _clean_query(query, keyword):
    query = query.replace("jarvis", "")
    query = query.replace(keyword, "")
    query = query.replace("search", "")
    query = query.replace("on", "")
    return query.strip()


def searchGoogle(query):
    if "google" in query:
        google_query = _clean_query(query, "google")
        speak("This is what I found on google")

        try:
            pywhatkit.search(google_query)
            result = wikipedia.summary(google_query, sentences=1)
            speak(result)
        except Exception:
            speak("No speakable output available")


def searchYoutube(query):
    if "youtube" in query:
        youtube_query = _clean_query(query, "youtube")
        speak("This is what I found for your search!")
        web = "https://www.youtube.com/results?search_query=" + youtube_query
        webbrowser.open(web)
        pywhatkit.playonyt(youtube_query)
        speak("Done, sir")


def searchWikipedia(query):
    if "wikipedia" in query:
        wikipedia_query = _clean_query(query, "wikipedia")
        speak("Searching from wikipedia...")

        try:
            results = wikipedia.summary(wikipedia_query, sentences=2, auto_suggest=False)
            speak("According to wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple Wikipedia results. Please say a more specific name.")
        except wikipedia.exceptions.PageError:
            speak("I could not find that page on Wikipedia.")
        except Exception as e:
            print("Wikipedia Error:", e)
            speak("Wikipedia is not responding properly right now.")
