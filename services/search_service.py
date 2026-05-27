import webbrowser
from urllib.parse import quote_plus

import pywhatkit
import wikipedia

from .speech import speak


FILLER_WORDS = {"jarvis", "search", "on", "for", "please"}


def clean_query(query, keyword):
    cleaned_words = []

    for word in query.lower().split():
        if word == keyword or word in FILLER_WORDS:
            continue
        cleaned_words.append(word)

    return " ".join(cleaned_words).strip()


def search_google(query):
    google_query = clean_query(query, "google")
    if not google_query:
        speak("Please say what you want me to search on google.")
        return

    speak("This is what I found on google")

    try:
        pywhatkit.search(google_query)
        result = wikipedia.summary(google_query, sentences=1)
        speak(result)
    except Exception:
        speak("No speakable output available")


def search_youtube(query):
    youtube_query = clean_query(query, "youtube")
    if not youtube_query:
        speak("Please say what you want me to search on youtube.")
        return

    speak("This is what I found for your search!")
    webbrowser.open("https://www.youtube.com/results?search_query=" + quote_plus(youtube_query))
    pywhatkit.playonyt(youtube_query)
    speak("Done, sir")


def search_wikipedia(query):
    wikipedia_query = clean_query(query, "wikipedia")
    if not wikipedia_query:
        speak("Please say what you want me to search on wikipedia.")
        return

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
    except Exception as error:
        print("Wikipedia Error:", error)
        speak("Wikipedia is not responding properly right now.")
