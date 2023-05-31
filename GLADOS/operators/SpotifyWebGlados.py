import os
import json
import spotipy
import speech_recognition
from speech_recognition import UnknownValueError
from GladosSoundLibrary import GladosSound
import spotipy.util as util
from json.decoder import JSONDecodeError
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pathlib
class SpotifyWebAPI:
    def __init__(self,login_id,password):
        self.login_id = login_id
        self.password=password
        os.chdir(pathlib.Path(__file__).parent.resolve())
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        self.driver_path = path_parent + r'\chromedriver.exe'

    def SpotifyWebGlados(self):
        recognizer = speech_recognition.Recognizer()
        spotify_url= "https://accounts.spotify.com/tr/login"
        options = webdriver.ChromeOptions() 
        options.add_experimental_option("detach", True)
        options.add_argument("user-data-dir=C:\\Path") 
        driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        driver.maximize_window()
        driver.get(spotify_url)
        #username
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/input").send_keys(self.login_id)
        #password
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/input").send_keys(self.password)
        #click login
        driver.find_element_by_css_selector('#login-button > div.ButtonInner-sc-14ud5tc-0.lbsIMA.encore-bright-accent-set > p').click()
        time.sleep(2)
        driver.find_element_by_css_selector('#root > div > div.sc-giYglK.ggrwSq > div > div > button.Button-y0gtbx-0.hpTULc.sc-iCfMLu.MPAeZ').click()
        time.sleep(2)
        while True:
            
            with speech_recognition.Microphone() as mic:
                    
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    recognizer.energy_threshold = 3000
                    audio = recognizer.listen(mic)
                    try:
                        songchoice = recognizer.recognize_google(audio,None,"tr-TR",show_all=False)
                        songchoice = songchoice.lower()
                        print('{}'.format(songchoice))
                    except speech_recognition.UnknownValueError:
                        print("Unknown Value")
                        recognizer = speech_recognition.Recognizer()
                        time.sleep(1)
                        continue
            if "kapat" in songchoice:
                driver.find_element_by_css_selector('#searchPage > div > div > section.QVIrLvegL13F9cEdMqfT.rjgEnbv42_EUDbaiZnA2 > div.iKwGKEfAfW7Rkx2_Ba4E > div > div > div > div:nth-child(2) > div:nth-child(1) > div > div.gvLrgQXBFVW6m9MscfFA > div.byLkljnIRd_DJeSMD3LM > button').click()
                time.sleep(2)
                driver.find_element_by_css_selector('#main > div > div.Root__top-container > div.Root__top-bar > header > button > figure > div > div').click()
                time.sleep(2)
                driver.find_element_by_css_selector('#context-menu > div > ul > li:nth-child(3) > button').click()
                time.sleep(2)
                driver.close()
            elif songchoice == "şarkıyı değiştir":
                driver.find_element_by_css_selector('#main > div > div.Root__top-container > div.Root__top-bar > header > div.rovbQsmAS_mwvpKHaVhQ > div > div > div > button').click()
                time.sleep(2)
                driver.find_element_by_css_selector('#main > div > div.Root__top-container > div.Root__main-view > div.main-view-container > div.os-host.os-host-foreign.os-theme-spotify.os-host-resize-disabled.os-host-scrollbar-horizontal-hidden.main-view-container__scroll-node.os-host-transition.os-host-overflow.os-host-overflow-y > div.os-padding > div > div > div.main-view-container__scroll-node-child > main > div.fVB_YDdnaDlztX7CcWTA > div > div > div > div.KjPUGV8uMbl_0bvk9ePv > a:nth-child(2) > button').click()
                time.sleep(2)
                
                with speech_recognition.Microphone() as mic:
                    
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    recognizer.energy_threshold = 3000
                    audio = recognizer.listen(mic)
                    try:
                        songchoice = recognizer.recognize_google(audio,None,"tr-TR",show_all=False)
                        songchoice = songchoice.lower()
                        print('{}'.format(songchoice))
                    except speech_recognition.UnknownValueError:
                        print("Unknown Value")
                        recognizer = speech_recognition.Recognizer()
                        time.sleep(1)
                        continue
                driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]").click()
                time.sleep(2) 
                driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]").click()
                time.sleep(2)      
            
            driver.find_element_by_css_selector('#main > div > div.Root__top-container > nav > div.tUwyjggD2n5KvEtP5z1B > ul > li:nth-child(2) > a').click()
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[1]/header/div[3]/div/div/form/input").send_keys(songchoice)
            time.sleep(4)
            #driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/section[1]/div[2]/div/div/div/div[3]/div/button/div").click()
            #time.sleep(2)
            driver.find_element_by_css_selector('#main > div > div.Root__top-container > div.Root__main-view > div.main-view-container > div.os-host.os-host-foreign.os-theme-spotify.os-host-resize-disabled.os-host-scrollbar-horizontal-hidden.main-view-container__scroll-node.os-host-transition.os-host-overflow.os-host-overflow-y > div.os-padding > div > div > div.main-view-container__scroll-node-child > main > div.fVB_YDdnaDlztX7CcWTA > div > div > div > div.KjPUGV8uMbl_0bvk9ePv > a:nth-child(2) > button').click()
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]").click()
            time.sleep(0.1)    
            driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/button").click()
            time.sleep(0.1)
            
            
            #Durdur-Başlat
            #driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]").send_keys(Keys.SPACE)
            #time.sleep(0.1)
            
            
            #searchPage > div > div > section.QVIrLvegL13F9cEdMqfT.EbZrO5qZMclA_AaI3NV8 > div.iKwGKEfAfW7Rkx2_Ba4E > div > div > div > div:nth-child(2) > div:nth-child(1) > div
