import pyjokes
import speech_recognition as sr
import pywhatkit
import pyttsx3
import yfinance as yf
import webbrowser
import datetime
import wikipedia
import pyaudio
import arabic_reshaper
from bidi.algorithm import get_display

engine= pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    print(f"ID: {voice.id}\nName: {voice.name}\nLanguages: {voice.languages}\n")

def speak(message):
    #start pyttsx3
    engine= pyttsx3.init()

    voices = engine.getProperty('voices')
    for voice in voices:
        if "ar" in voice.languages:  
            # Vérifie si la voix prend en charge l'arabe
            engine.setProperty('voice', voice.id)
            break
    else:
        print("Aucune voix arabe trouvée. Assurez-vous qu'une voix arabe est installée.")


    #deliver message
    engine.say(message)
    engine.runAndWait()


speak('مرحبا، كيف حالك؟')