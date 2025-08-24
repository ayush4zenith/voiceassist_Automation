import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import psutil
import pyjokes
import requests
import json
import random

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
GEMINI_API = os.getenv("GEMINI_API_KEY")
WEATHER_API = os.getenv("WEATHER_API_KEY")
NEWS_API= os.getenv("NEWS_API_KEY")
MUSIC_DIR = os.getenv("MUSIC_DIR")
WORD_PATH = os.getenv("WORD_PATH")

# Initialize the engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # voice[0] is male, voice[1] is female
engine.setProperty('rate', 170) # change the speed of speech as needed

def speak(text):
    try:
        print(f"Aarvy: {text}")
    except UnicodeEncodeError:
        print(f"Aarvy: {text.encode('ascii', 'ignore').decode()}")  # Removes unsupported characters
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning Sir!")
    elif hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')  # change the language as per needs
        print(f"You said: {query}")
    except Exception:
        # speak("Sorry, I didn't catch that. Please say that again.")
        return "none"
    return query.lower()

def open_website(site_name, url):
    speak(f"opening {site_name}")
    webbrowser.open(url)

def open_app(app_name, app_path):
    speak(f"Openning {app_name}")
    try:
        os.startfile(app_path)
    except FileNotFoundError:
        speak(f"Sorry, I couldn't find the application {app_name}. Please check the path.")
def get_battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"Battery is at {percent} percent.")
    if battery.power_plugged:
        speak("Charger is connected.")
    else:
        speak("Charger is not connected.")

def tell_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time}")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    print(joke)

def play_music():

    songs=os.listdir(MUSIC_DIR)
    if songs:
        song=random.choice(songs)
        song_path=os.path.join(MUSIC_DIR, song)
        os.startfile(song_path)
        speak(f"Playing {song}")

    else:
        speak("No songs found in the music directory.")
    
def get_weather(city):  
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    complete_url = f"{base_url}appid={WEATHER_API}&q={city}&units=metric"
    try:
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] != "404":  
            weather = data["main"]
            temp = weather["temp"]
            feels_like = weather["feels_like"]
            description = data["weather"][0]["description"]
            
            report = f"The temperature in {city} is {temp}°C. It feels like {feels_like}°C with {description}."
            speak(report)
        else:
            speak("City not found. Please try again.")
    except:
        speak("Sorry, I couldn't fetch the weather right now.")

def get_news(country, category):
    base_url = "http://api.mediastack.com/v1/news"

    params = {
        "access_key": NEWS_API,
        "countries": country,
        "languages": "en",
        "limit": 5
    }
    if category:
        params["categories"] = category   # e.g., "sports", "business", "technology"

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            articles = data["data"]
            speak(f"Here are the latest top headlines from {country.upper()} in {category.upper()}:")
            for i, article in enumerate(articles, 1):
                headline = article["title"]
                print(f"{i}. {headline}")
                speak(headline)
        else:
            speak("Sorry, I couldn't find any latest news right now.")
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("Sorry, I'm having trouble fetching the news at the moment.")

def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)

def save_to_memory():
    speak("What should I store, sir?")
    data = take_command()
    if " is " in data:
        key, value = data.split(" is ", 1)
        key = key.strip().lower()
        cleaned_key = key.replace("my ", "").replace("your ", "").replace("the ", "").strip()
        value = value.strip()
        memory = load_memory()
        memory[cleaned_key] = value
        save_memory(memory)
        speak(f"I've saved that your {cleaned_key} is {value}.")
    else:
        speak("Sorry, I couldn't understand. Use the format like 'my birthday is 5th July' or 'my school is xyz'.")

def retrieve_from_memory(query):
    memory = load_memory()
    found = False
    for key in memory:
        if key in query:
            speak(f"Your {key} is {memory[key]}")
            found = True
            break
    if not found:
        speak("I couldn't find that information in memory.")

def createFile():
    speak("What should I name the file?")
    file_name = take_command()
    if file_name == "none":
        speak("I didn't catch that. Please try again.")
        return
    file_name = file_name.replace(" ", "_") + ".txt"  # Replace spaces with underscores
    with open(file_name, "w") as f:
        speak(f"File {file_name} created successfully. What should I write in it?")
        content = take_command()
        f.write(content)
    speak(f"I've written your content in {file_name}.")

def get_gemini_response(prompt):
    
    # speak("Let me think about that...")
    chatHistory = []
    instruction = "Answer briefly and in simple words. Limit your response to 2-3 lines."
    full_prompt = f"{prompt}\n\n{instruction}"
    chatHistory.append({"role": "user", "parts": [{"text": full_prompt}]})
    payload = {"contents": chatHistory}
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API}"

    try:
        response = requests.post(apiUrl, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status() 
        result = response.json()
        
        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return text
        else:
            print("Unexpected API response structure:", result)
            return "I'm sorry, I couldn't get a clear response from the AI."
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm having trouble connecting to the internet right now."
    except json.JSONDecodeError:
        print("Error decoding JSON response from Gemini API.")
        return "I received an unreadable response from the AI."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "I encountered an unexpected issue while processing your request."


# Main function
if __name__ == "__main__":
    wish_me()
    speak("I am Aarvy. How may I help you today?")

while True:
    query = take_command()

    # Prioritize exit/quit commands
    if query == "none":
        pass
    elif 'name' in query:
        speak("I am Aarvy, your personal voice assistant.")
    elif 'greet' in query or 'hello' in query:
        wish_me()
    elif 'what do you do' in query or 'your function' in query:
        speak("I can assist you with various tasks like opening websites, telling jokes, providing weather updates, playing music, and much more.")
    elif 'exit' in query or 'quit' in query or 'bye' in query or 'goodbye' in query:
        speak("Goodbye, Sir!")
        break
    elif 'weather' in query:
        get_weather("Indore")
    elif 'news' in query or 'headlines' in query:
        get_news("in","technology")  
    elif 'open youtube' in query:
        open_website("YouTube", "https://www.youtube.com")
    elif 'open google' in query:
        open_website("Google", "https://www.google.com")
    elif 'open chatgpt' in query or 'open chat gpt' in query:
        open_website("ChatGpt", "https://www.chatgpt.com")
    elif 'open linkedin' in query:  
        open_website("LinkedIn", "https://www.linkedin.com")
    elif 'open facebook' in query:
        open_website("Facebook", "https://www.facebook.com")
    elif 'open cambridge dictionary' in query:
        open_website("Cambridge Dictionary", "https://dictionary.cambridge.org")
    elif 'open stack overflow' in query:
        open_website("Stack Overflow", "https://stackoverflow.com")
    elif 'open word' in query or 'open ms word' in query:
        open_app("Microsoft Word", WORD_PATH)
    elif 'what is the time' in query or 'tell me the time' in query:
         tell_time()
    elif 'play music' in query or 'start music' in query or 'play a song' in query or 'play song' in query or 'play something' in query:
         play_music()
    elif 'battery' in query or 'is laptop charging' in query:
        get_battery_status()
    elif 'joke' in query:
        tell_joke()
    elif 'nice' in query or 'nice one' in query or 'good job' in query:
        speak("Thank you, Sir! I'm here to assist you.")
    elif 'save' in query or 'store' in query:
        save_to_memory()
    elif 'create a file' in query or 'make file' in query or 'write file' in query:
        createFile()
    elif 'list memory' in query or 'show memory' in query or 'what you remember' in query:
        memory = load_memory()
        if memory:
            speak("Here's what I remember:")
            for key, value in memory.items():
                speak(f"Your {key} is {value}")
        else:
                speak("I don't have anything stored yet.")
    else:
        # Try retrieving from memory
        memory = load_memory()
        match_found = False
        for key in memory:
            if key in query:
                speak(f"Your {key} is {memory[key]}")
                match_found = True
                break
        if not match_found:
            # Use Gemini AI as fallback
            response_from_gemini = get_gemini_response(query)
            speak(response_from_gemini)
            

