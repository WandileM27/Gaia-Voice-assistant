from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
activation_Word = "Wednesday"

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

app_id = "EU3HEJ-JW6Q6PR558"
wolfram_client = wolframalpha.Client(app_id)


def Gaia_foundation():
    while True:
        query = get_command().lower().split()

        if query[0] == "say":
            if "hello" in query:
                pyttsx3.speak("Greetings, father")
            else:
                query.pop()
                speech = " ".join(query)
                pyttsx3.speak(speech)

        if query[0] == "go" and query[1] == "to":
            pyttsx3.speak("Opening...")
            query = " ".join(query[2:])
            webbrowser.get("chrome").open_new(query)

        if query[0] == "wikipedia":
            query = " ".join(query[1:])
            pyttsx3.speak("Querying wikipedia")
            pyttsx3.speak(search_wikipedia(query))

        if query[0] == "compute" or query[0] == "computer":
            query = " ".join(query[1:])
            pyttsx3.speak("Computing")
            try:
                result = search_wolframalpha(query)
                pyttsx3.speak(result)
            except:
                pyttsx3.speak("Unable to compute")

        if query[0] == "log":
            take_notes()

        if query[0] == "shut" and query[1] == "down":
            pyttsx3.speak("Shutting down")
            break


def speech(text, rate=120):
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()


def get_command():
    listener = sr.Recognizer()
    print("Listening for command...")

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print("Recognizing speech...")
        query = listener.recognize_google(input_speech, language="eg_gb")
        print(query)

    except Exception as exception:
        print("I did not quite catch that")
        pyttsx3.speak("I did not quite catch that")
        print(exception)
        return None
    return query


def search_wikipedia(query=""):
    search_results = wikipedia.search(query)
    if not search_results:
        print("no results found")
        return "no results received"
    try:
        wikipage = wikipedia.page(search_results[0])
    except wikipedia.DisambiguationError as error:
        wikipage = wikipedia.page(error.options[0])
    print(wikipage.title)
    wiki_summary = str(wikipage.summary)
    return wiki_summary


def list_or_dict(var):
    if isinstance(var, list):
        return var[0]["plaintext"]
    else:
        return var["plaintext"]


def take_notes():
    pyttsx3.speak("Ready to record note")
    new_note = get_command().lower()
    now = datetime.now().strftime('%H-%M-%S-%Y-%m-%d')
    with open("not_%s.txt" % now, "w") as new_file:
        new_file.write(new_note)
    pyttsx3.speak("note written")


def search_wolframalpha(query=""):
    response = wolfram_client.query(query)

    if response["@success"] == "false":
        return "Could not compute"

    else:
        result = ""
        pod0 = response["pod"][0]
        pod1 = response["pod"][1]

        if ("result" in pod1["@title"].lower()) or (pod1.get("@primary", "false") == "true") or (
                "definition" in pod1["@title"].lower()):

            result = list_or_dict(pod1["subpod"])

            return result.split("(")[0]
        else:
            question = list_or_dict(pod0["subpod"])
            pyttsx3.speak("computing failed, querying Wikipedia")
            return question.split("(")[0], search_wikipedia(question)


if __name__ == "__main__":
    pyttsx3.speak("Welcome Sir")
    Gaia_foundation()


