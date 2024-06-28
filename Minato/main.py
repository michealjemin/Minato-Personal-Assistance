import os
import datetime
import wikipedia
import webbrowser
import speech_recognition as sr
import pyttsx3
import pyowm
import requests

def speak(text):
    """Function to convert text to speech using pyttsx3"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Function to wish the user based on the time of the day"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("I am Minato, your advanced personal assistant. How can I assist you today?")

def listen_command():
    """Function to listen to user's command using speech recognition"""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=5)  # Adjust duration as needed
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Adjust energy threshold if needed
        command = recognizer.recognize_google(audio, language="en-US")
        print(f"User said: {command}")
        return command.lower()

    except sr.UnknownValueError:
        print("Sorry, I did not understand that. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def process_command(command):
    """Function to process user's command"""
    if "wikipedia" in command:
        speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia, ")
        speak(results)

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com/")

    elif "open google" in command:
        webbrowser.open("https://www.google.com/")

    elif "open code" in command:
        os.system("code")  # Open Visual Studio Code. Adjust this based on your preferred code editor.

    elif "tell me about" in command:
        # Assuming summarizer is defined somewhere in your code
        topic = command.replace("tell me about", "").strip()
        response = summarizer(topic, max_length=150, min_length=50, length_penalty=2.0, num_beams=4,
                              early_stopping=True)
        speak(response[0]['summary'])

    elif "who are you" in command:
        speak("I am Minato , an personal assistance for Arun.")

    elif "what's the weather" in command:
        get_weather()

    elif "what's the time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M %p")
        speak(f"The current time is {current_time}")

    elif " can joke" in command:
        # Integrate with a joke API to provide a random joke
        speak("I'm sorry, I am not your wife.")

    elif "play music" in command:
        # You can integrate with a music service API to play music
        speak("I'm sorry, music functionality is not implemented yet.")

    elif "your name" in command:
        speak("I am Minato, your personal assistant.")

    elif "exit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I'm sorry, I don't understand that command. Please try again.")

def get_weather():
    speak("Sure, let me check the weather for you.")
    weather_api_key = "c268edd364b060f485bd20c153d15e9f"  # Replace with your actual API key
    city = "pondicherry,India"  # Replace with the desired location (e.g., "New York, US")

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    response = requests.get(weather_url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        speak(f"The current temperature is {temperature} Kelvin, and the weather is {weather_description}.")
    else:
        speak("I'm sorry, I couldn't retrieve the weather information at the moment.")


if __name__ == "__main__":
    wish_me()

    while True:
        command = listen_command()

        if command:
            process_command(command)
