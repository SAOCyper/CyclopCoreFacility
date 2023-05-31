import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import speech_recognition
from speech_recognition import UnknownValueError
from speech_recognition import UnknownValueError
from GladosSoundLibrary import GladosSound
from SpeechSynthesis import GladosTTS,GladosListenWithoutAI

class SpotifyGlados():
    def __init__(self,spotify_username):
        self.listen = GladosListenWithoutAI()
        self.listen = self.listen.Glados_listen
        self.speak = GladosTTS.Gladostts
        self.username = spotify_username
        self.scope = 'user-read-private user-read-playback-state user-modify-playback-state'
        self.clientID = '51c28880318a4452a3830d69dfcba2bf'
        self.clientSecret = 'a8c86c79e1bf4549a14206a4bc39b760'
        self.redirectURI = 'http://localhost:8000'
        self.oauth_object = spotipy.SpotifyOAuth(self.clientID,self.clientSecret,self.redirectURI)
        self.token_dict = self.oauth_object.get_access_token()
        self.token = self.token_dict['access_token']
        try:
            self.token = util.prompt_for_user_token(self.username,self.scope,self.clientID,self.clientSecret,self.redirectURI)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{self.username}")
            self.token = util.prompt_for_user_token(self.username,self.scope,self.clientID,self.clientSecret,self.redirectURI)
        # Create Spotify object
        self.spotifyObject = spotipy.Spotify(auth=self.token)
        self.user = self.spotifyObject.current_user()
        self.devices = self.spotifyObject.devices()
        self.deviceID = self.devices['devices'][0]['id']
        self.displayName = self.user['display_name']
        print(json.dumps(self.devices, sort_keys=True, indent=4))
        
    def Glados_spotify(self,text):
        self.artistchoice = None
        choice = text
        while True:
            if choice != "spotify kapat":
                self.speak(f"Welcome to Spotify {self.displayName} ")
            if choice == "spotify ac":
                while True:
                    self.speak("Please choose an artist to display")
                    while self.artistchoice == None or self.artistchoice == "Unknown Value":
                        self.artistchoice=self.listen()
                        if self.artistchoice == "Unknown Value":
                            continue
                        else :
                            break
                    query = self.artistchoice
                    searchResults = self.spotifyObject.search(query,1,0,"artist")
                    # Print artist details
                    artist = searchResults['artists']['items'][0]  
                    if len(artist['name'])>0:
                        self.speak(f"Artist name {self.artistchoice} is choosen")
                    artistID = artist['id']
                    # Album details
                    trackURIs = []
                    trackURIs2 = {}
                    z = 0
                    # Extract data from album
                    albumResults = self.spotifyObject.artist_albums(artistID)
                    albumResults = albumResults['items']

                    for item in albumResults:
                        print("ALBUM: " + item['name'])
                        albumID = item['id']
                        # Extract track data
                        trackResults = self.spotifyObject.album_tracks(albumID)
                        trackResults = trackResults['items']

                        for item in trackResults:
                            print(str(z) + ": " + item['name'].lower())
                            trackURIs.append(item['uri'])
                            trackURIs2[item['name'].lower()] = item['uri']
                            z+=1
                        print()
                    # See album art
                    songselection = None
                    while True:
                        if songselection == None :
                            self.speak("Please choose song to play")
                        while songselection == None or songchoice == "Unknown Value":
                            recognizer = speech_recognition.Recognizer()
                            with speech_recognition.Microphone() as mic:
                                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                                recognizer.energy_threshold = 3000
                                audio = recognizer.listen(mic)
                                try:
                                    songchoice = recognizer.recognize_google(audio,None,"tr-TR",show_all=False)
                                    songchoice=songchoice.lower()
                                    print('{}'.format(songchoice))
                                    trackSelectionList = []
                                    #trackSelectionList.append(trackURIs[songchoice])
                                    song = trackURIs2.get(songchoice)
                                    trackSelectionList.append(song)
                                    if songchoice in trackURIs2:
                                        self.speak(f"Playing {songchoice} ")
                                        self.spotifyObject.start_playback(self.deviceID, None,trackSelectionList)
                                    elif songchoice == "sanatçı değiştir": 
                                        break
                                    elif songchoice == "şarkı değiştir":
                                        continue
                                    elif songchoice == "spotify kapat":
                                        self.speak(f"Closing Spotify.Goodbye {self.displayName}")
                                        break
                                    else:
                                        continue
                                except speech_recognition.UnknownValueError:
                                    print("Unknown Value")
                                    recognizer = speech_recognition.Recognizer()
                                    continue
                        if songchoice == "spotify kapat":
                            choice =songchoice
                            break 
                        
                        elif songchoice == "sanatçı değiştir":
                            self.artistchoice=None
                            break
                    if choice == "spotify kapat":
                        break
                    else:       
                        continue
            # End program
            elif choice == "spotify kapat":
                self.spotifyObject.pause_playback(self.deviceID)
                break
