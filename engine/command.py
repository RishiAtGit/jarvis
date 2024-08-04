import datetime
import json
import os
import random
from bs4 import BeautifulSoup
import pyttsx3
import requests
import speech_recognition as sr
import eel
import time
import speedtest
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
           from engine.features import openCommand
           openCommand(query)               
        
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query) 
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)
                
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speak(f"Sir time is {hour} bajjke {min} minute")
        

        elif "google" in query:
            from engine.features import searchGoogle
            searchGoogle(query)

        elif "youtube" in query:
            from engine.features import searchYoutube
            searchYoutube(query)
        
        elif "wikipedia" in query:
            from engine.features import searchWikipedia
            searchWikipedia(query)

        elif "temperature" in query:
            search = "temperature in bokaro"
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            speak(f"current{search} is {temp}")
        elif "weather" in query:
            search = "weather in bokaro"
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            speak(f"current{search} is {temp}")
        
        elif "news" in query:
            api_dict = {"business" : "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=e74d5cf32fd14525b354918e6b1bdd98",
            "entertainment" : "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=e74d5cf32fd14525b354918e6b1bdd98",
            "health" : "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=e74d5cf32fd14525b354918e6b1bdd98",
            "science" :"https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=e74d5cf32fd14525b354918e6b1bdd98",
            "sports" :"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=e74d5cf32fd14525b354918e6b1bdd98",
            "technology" :"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=e74d5cf32fd14525b354918e6b1bdd98"
          }

            content = None
            url = None
            speak("Which field news do you want, [business] , [health] , [technology], [sports] , [entertainment] , [science]")
            field = takecommand()
            for key ,value in api_dict.items():
                if key.lower() in field.lower():
                    url = value
                    print(url)
                    print("url was found")
                    break
                else:
                    url = True
            if url is True:
                print("url not found")

            news = requests.get(url).text
            news = json.loads(news)
            speak("Here is the news.")

            arti = news["articles"]
            for articles in arti :
                article = articles["title"]
                print(article)
                speak(article)
                news_url = articles["url"]
                print(f"for more info visit: {news_url}")

        elif "internet speed" in query:
                    wifi  = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")
        
        
        elif "play game" in query:
            speak("Lets Play ROCK PAPER SCISSORS !!")
            print("LETS PLAYYYYYYYYYYYYYY")
            i = 0
            Me_score = 0
            Com_score = 0
            while(i<5):
                choose = ("rock","paper","scissors") #Tuple
                com_choose = random.choice(choose)
                query = takecommand().lower()
                if (query == "rock"):
                    if (com_choose == "rock"):
                        speak("ROCK")
                        print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                    elif (com_choose == "paper"):
                        speak("paper")
                        Com_score += 1
                        print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                    else:
                        speak("Scissors")
                        Me_score += 1
                        print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

                elif (query == "paper" ):
                    if (com_choose == "rock"):
                        speak("ROCK")
                        Me_score += 1
                        print(f"Score:- ME :- {Me_score+1} : COM :- {Com_score}")

                    elif (com_choose == "paper"):
                        speak("paper")
                        print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                    else:
                        speak("Scissors")
                        Com_score += 1
                        print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")

                elif (query == "scissors" or query == "scissor"):
                    if (com_choose == "rock"):
                        speak("ROCK")
                        Com_score += 1
                        print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                    elif (com_choose == "paper"):
                        speak("paper")
                        Me_score += 1
                        print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                    else:
                        speak("Scissors")
                        print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                i += 1

            print(f"FINAL SCORE :- ME :- {Me_score} : COM :- {Com_score}")

        else:
            from engine.features import chatBot
            chatBot(query)

    except:
        print("error")
    
    eel.ShowHood()