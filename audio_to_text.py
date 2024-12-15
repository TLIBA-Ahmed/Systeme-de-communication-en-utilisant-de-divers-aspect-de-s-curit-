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


# 1/ écouter le vocal et renvoyer l'audio sous forme de texte

def transform_audio_into_text():
    # stocker le capteur dans une variable
    r= sr.Recognizer()

    #set microphone
    with sr.Microphone() as source:

        
        # pour tous type de probleme de volume et retard par l'utilisateur 
        r.pause_threshold = .8

        # annoncer que l'enregistrement a commencé
        print('Vous pouvez maintenant parler')

       
        audio = r.listen(source)

        try:
            #recherche dans google
            request = r.recognize_google(audio , language="ar-TN")

            #formater le texte arabe pour un affichage correct
            reshaped_text = arabic_reshaper.reshape(request)
            bidi_text = get_display(reshaped_text)

            #test in text
            print('"' + bidi_text+'"')

            return request
        
        except sr.UnknownValueError:
            print("Ups! I didn't understand audio")

            return "I am still waiting"
        
        except sr.RequestError:
            print("Ups! I didn't understand audio")

            return "I am still waiting"
        
        except:
            print("Ups! Something went wrong !!")

            return "I am still waiting"
        

#transform_audio_into_text()


