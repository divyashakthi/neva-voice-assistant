import os
import time
import pyttsx3
import datetime
import playsound 
import speech_recognition as sr
from gtts import gTTS
import random
import webbrowser
import pyowm
import sys
from time import sleep
import subprocess
#import pygame
import pywhatkit
#from flask import Flask
import spotipy
import cv2

#converting text to audio
def speak(audio_inp):
    c=pyttsx3.init()
    newVoiceRate = 145
    c.setProperty('rate',newVoiceRate)
    voice_id="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    #voice_id="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enUS_MarkM"
    c.setProperty('voice',voice_id )
    c.runAndWait()
    c.say(audio_inp)
    c.runAndWait()
    
#converting audio to text    
def audio():
    r=sr.Recognizer()
    r.energy_threshold = 4000
    with sr.Microphone(device_index=1) as source:
        r.adjust_for_ambient_noise(source,duration=0.5)
        print("speak now")
        aud=r.listen(source)
        var=""
    try:
        var=r.recognize_google(aud)
    except sr.UnknownValueError:
        var="could not understand audio, would you try saying that again?"
        text=audio()
    except sr.RequestError:
        var=" Looks like, there is some problem with Google Speech Recognition"
        
    return var
    
    
speak(" hi how can i help you?")

text=audio()
print(text)
    
while(text not in ["thank you","exit"]):
    #responding
    if text in ["hi","hai"]:
        speak("hello, how are you doing today")
        text=audio()
    if text in ["name","what's your name"]:
        speak("my name is nayva")
        text=audio()
    if text in ["compliment","complement","give me a compliment","give me a complement"]:
        c=["You have the best laugh","you light up the room","you look really great today","You're like sunshine on a rainy day"]
        speak(random.choice(c))
        text=audio()

    #web search
    if text in ["search","open google","google search","open Google","Google search"]:
        speak("what do you want to search?")
        sd=audio()
        url="https://google.com/search?q="+sd
        webbrowser.get().open(url)
        speak("this is what i found for" + sd)
        text=audio()

    #remainder    
    if text in ["remind me","give me a reminder"]:
        
        speak(" How frequent do you want me to give you a reminder?")
        rem_chc=audio()
        print(rem_chc)
        speak("I will remind you in " + rem_chc)

        acc=audio()
        rem_freq=0
        if acc in ["ok","okay","sure"]:
            if rem_chc in ["seconds","second"]:
                secs=0
                for i in rem_chc:
                    if i.isdigit():
                        secs=int(i)
                rem_freq=secs/60
            if "minutes" in rem_chc:
                mint=0
                for i in rem_chc:
                    if i.isdigit():
                        mint=int(i)
                rem_freq=mint/60
                        
            if "hours" in rem_chc:
                hr=0
                for i in rem_chc:
                    if i.isdigit():
                        hr=int(i)
                rem_freq=hr/60   
        else:
            speak("Please restart me in order to choose another number. I am still not that complicated")
            sys.exit()
        print("starting",rem_freq)

        while rem_freq > 0:
            sleep(60*60*rem_freq) 
            speak("Hey! its time to take the much needed break, now!")
            speak("Would you like to listen to some music?")
            ans=audio()
            if "yes" or "yeah" in ans:
                    music()   

    #playing youtube videos
    if text in ["video","open youtube","open you tube","play a video"]:
        speak("what video do you want to watch?")
        vid=audio()
        yt_url="https://www.youtube.com/results?search_query="+vid
        webbrowser.open(yt_url)
        speak("here's what i found for"+vid+"videos")
        text=audio()

    #finding a location in google maps
    if text in["location","what's my current location","my location"]:
        speak("what location do you want to find")
        lct=audio()
        webbrowser.open('https://www.google.co.in/maps/place/'+lct)
        text=audio()

    #weather forecast
    if text in ["what's the weather forecast","weather","weather forecast"]:
        o=pyowm.OWM("4f64378314b5aae75020286aadb3bc65")
        city="Chennai"
        l=o.weather_manager().weather_at_place(city)
        w=l.weather
        t=w.temperature(unit='celsius')
        l=[]
        for k,v in t.items():
            if v!=None:
                    tm=""
                    tm=str(v)
                    d=tm+" "+"degree celsius"
                    l.append(d)
        det=["Temperature is ","Maximum temperature is ","Minimum temperature is ","Feels like "]
        fd=[]
        for i in range(4):
            fd.append(det[i]+l[i])
        for j in fd:
            speak(j)
        text=audio()

    #making a note
    def note(text):
        d=datetime.datetime.now()
        fn=str(d).replace("."," ").replace(":"," ")+" note.txt"
        with open(fn,"w") as f:
            f.write(text)
        subprocess.Popen(["notepad.exe",fn])
            
    if text in ["note","make a note"]:
        speak("what do you want me to make a note of?")
        wt=audio()
        note(wt)
        text=audio()

    def music():
        username='31eoapdgbljq5senrefpgrw7tecm'
        client_id='d18d14b53e434114b1f7e2494a5cd9eb'
        client_secret='526cbebf590143fa8957a18a910d4922'
        redirect='http://google.com/'
        oauth_object=spotipy.SpotifyOAuth(client_id,client_secret,redirect)
        token_dict=oauth_object.get_cached_token()
        token=token_dict['access_token']
        spotify_object=spotipy.Spotify(auth=token)
        user=spotify_object.current_user()
        speak("what would you like to listen to?")
        spo=audio()
        speak("this is what i found for"+spo)
        search_res=spotify_object.search(spo,1,0,"track")
        tracks_dict=search_res['tracks']
        tracks_items=tracks_dict['items']
        song=tracks_items[0]['external_urls']['spotify']
        webbrowser.open(song)
        print('Requested song has been opened in your browser woohoo!!!')
        text=audio()
    
    #playing music on spotify
    if text in["music","play music","open spotify"]: 
        music()

    #taking pictures using front camera
    if text in ["picture","take a picture"]:
        cam_port = 0
        speak("say cheese!")
        cam = cv2.VideoCapture(cam_port)
        result, image = cam.read()
        if result:
            cv2.imshow("hehehe", image)
            cv2.imwrite("hehehe.png", image)
            cv2.waitKey(0)
            cv2.destroyWindow("hehehe")
            text=audio()
        else:
            speak("No image detected. Please! try again")
            text=audio()
        