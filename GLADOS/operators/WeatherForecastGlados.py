import json
import requests
import os 
from dataclasses import dataclass
import factory 
from SpeechSynthesis import GladosTTS,GladosListenWithoutAI
class GladosWeatherForecast:
    def __init__(self):
        self.API_KEY =os.getenv('WEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.listen = GladosListenWithoutAI()
        self.listen = self.listen.Glados_listen
        self.speak = GladosTTS.Gladostts
    def WebScraper(self,city_name):
        
        complete_url = self.base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name
        response = requests.get(complete_url)
        x=response.json()
        if x["cod"] != "404":
            y = x["main"]
            city=x["name"]
            current_temperature = y["temp"]
            max_temparature = y["temp_max"]
            min_temparature = y["temp_min"]
            humidity = y["humidity"]
            z = x["weather"]
            degree=current_temperature - 273.15
            Degree = "%.2f"%degree
            max_degree = max_temparature - 273.15
            min_degree = min_temparature - 273.15
            Max_degree = "%.2f"%max_degree
            Min_degree = "%.2f"%min_degree
            weather_description = z[0]["description"]
            ZIP_LIST = [{"city" : city,"Degree":Degree,"Min_temperature" :Min_degree,"Max_temperature" : Max_degree,"Condition" : weather_description,"humidity":humidity},
                        {"city" : city,"Degree":Degree,"Min_temperature" :Min_degree,"Max_temperature" : Max_degree,"Condition" : weather_description,"humidity":humidity}]
            return ZIP_LIST
        else:
            print(" City Not Found ")

class Weather_skill:
    
    def handle_command(command:str = None):
        myweather = GladosWeatherForecast()
        myweather.speak("Please choose the city you wish to know")
        city_name=myweather.listen()
        myweather.speak("Fetching today's weather condition")
        Weather_Info = myweather.WebScraper(city_name=city_name)
        myweather.speak("{} city,current temperature is {} celcius,minimum and maximum temperature is {} celcius and {} celcius,weather condition is {} and humidity level is at {} ".format(Weather_Info[0]["city"],Weather_Info[0]["Degree"],Weather_Info[0]["Min_temperature"],Weather_Info[0]["Max_temperature"],Weather_Info[0]["Condition"],Weather_Info[0]["humidity"]))
        return Weather_Info
