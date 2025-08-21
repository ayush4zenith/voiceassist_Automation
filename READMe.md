🎙 Voice-Controlled Python Assistant

Ever wished your computer could just listen and get things done for you?
This Voice-Controlled Assistant, built using Python, automates your everyday desktop tasks with simple voice commands — all running locally on your system.

🔧 Features

🎵 Play local music

📁 Create and write to files

🌐 Search Google directly

🖥 Open apps like Google, Youtube, etc.

📊 Check system info (CPU, battery, etc.)

🕹 Fully voice-activated interaction

📰 Smart Updates 


🛠 Tech Stack

Python 3

speech_recognition – for voice input

pyttsx3 – for speech output

os, webbrowser, psutil, datetime, etc. – for system-level tasks

Runs locally using VS Code or any Python IDE

⚙️ How it Works??

•Voice Input & Output
Uses speech recognition to understand spoken commands in English and Hindi and text to speech to reply.
Responds with realistic text-to-speech output for a Jarvis-like feel.

•System & Utility Tasks
Opens websites, applications, and files on command.
Plays music from local storage or online.
Checks internet speed, battery status, and system information.

•Smart Memory
Can remember information you tell it (e.g., notes, reminders, personal details).
Retrieves saved information when asked.

•Knowledge & APIs
Uses Gemini API to answer general questions, explain concepts, or assist with tasks.
Can tell jokes, provide facts, and hold interactive conversations.

•Continuous Loop
Runs persistently, always listening for commands.
Executes the appropriate action based on recognized intent.

🚀 How to Run?

1. Clone the repository

git clone https://github.com/ayush4zenith/voiceassist_Automation.git

2. Install dependencies
pip install -r req.txt

3. Run the script
python task.py

4. Speak a command, Try saying:

“create a file”
“Open Google"
"what is the time"
"battery"
“play music”
“search for Python tutorials on google”
"weather"
"store in memory"
"open youtube"

📌 Requirements

Python 3.x

Internet (for web search tasks)

Working microphone

VS Code or any Python-compatible IDE

🔑 API Setup
To make the assistant fully functional, add your own API keys for Gemini (Google Generative AI), Mediastack (news), and OpenWeather (weather) in a `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key_here
NEWS_API_KEY=your_mediastack_api_key_here
WEATHER_API_KEY=your_openweather_api_key_here
```
You can get these keys by signing up at the respective service websites. This enables all smart features (AI answers, news, weather) to work for you.

🗂️ App Paths Setup
To use features like opening Microsoft Word or playing music, update the file paths in `task.py` to match your system:

- **Music Directory Example:**
	`C:\Users\your_username\Music` or any folder containing your songs

Edit these paths in the code to match your own computer for best results.

🎯 Use Cases

Boost productivity with voice automation

Hands-free access to routine tasks

Great for learning how speech and system automation work together

🤝 Contribute
Got an idea to improve or extend this assistant (like adding email, WhatsApp automation, or more)?
Feel free to fork, contribute, or raise an issue.

📬 Contact
Have suggestions or feedback? Reach out via LinkedIn or drop an issue here!

⭐ Star this repo
If you find this project helpful, consider starring it. 
