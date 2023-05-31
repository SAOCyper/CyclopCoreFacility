from dataclasses import dataclass
from fileinput import filename
from ics import Calendar,Event
from pathlib import Path
import os
import yaml
from datetime import datetime
from dateutil.relativedelta import *
import pytz
import dateparser
from datetime import datetime
from SpeechSynthesis import GladosTTS,GladosListen,GladosListenWithoutAI
import factory
import pathlib,os
import nltk
from nltk.stem import WordNetLemmatizer
pathfile=pathlib.Path(__file__).parent.resolve()
os.chdir(pathfile)
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
calendar_filename = path_parent + r'\GLADOS\myfile.ics'
calendar_datafile=path_parent + r'\GLADOS\myfile.yml'
print(calendar_datafile)
class GladosCalendar():
    c = Calendar()

    def __init__(self):
        ''' Print a nice banner'''
        self.listen=GladosListenWithoutAI()
        print("")
        print("*" * 80)
        print("Calendar Skill Loaded")
        print("*" * 80)
        

    def add_event(self,begin:str,name:str,description:str = None)->bool:
        '''Adds an event to the calendar'''
        e = Event()
        e.name = name
        e.begin = begin
        e.description = description
        try : 
            self.c.events.add(e)
            return True
        except:
            print("there was a problem while adding the event")
            return False
        
    def remove_event(self,event_name:str):
        '''Removes the event from calendar'''
        for event in self.c.events:
            if event.name == event_name:
                self.c.events.remove(event)
                print("removing event:",event_name)
                return True
        print("Sorry could not find that event",event_name)
        return False

    def parse_to_dict(self):
        dict = []
        for event in self.c.events:
            my_event = {}
            my_event['begin'] = event.begin.datetime
            my_event['name'] = event.name
            my_event['description'] = event.description
            dict.append(my_event)
        return dict

    def save(self):
        with open(calendar_filename,'w') as my_file:
            my_file.writelines(self.c)

        if self.c.events == set():
            print("No events - Removing YAML File")
            try:
                os.remove(calendar_datafile)
            except:
                print("Couldn't delete YAML File")
        else :
            with open(calendar_datafile,'w') as outfile:
                yaml.dump(self.parse_to_dict(),outfile,default_flow_style=False)

    def load(self):
        '''Load the Calendar data from the YAML file'''
        filename = calendar_datafile
        my_file = Path(filename)

        if my_file.is_file():
            stream = open(filename,'r')
            events_list = yaml.load(stream,Loader=yaml.Loader)
            for item in events_list:
                e = Event()
                e.begin = item['begin']
                e.description = item['description']
                e.name = item['name']
                self.c.events.add(e)
        else:
            print("File does not exist")

    def list_events(self,period:str=None)->bool:
        '''
            Lists the upcoming events if the 'period' is left empty it will default to today other options are:
            'tum'  -  lists all events in the calendar,
            'hafta'  -  lists all the events this week,
            'ay'  -  lists all the events this month
        '''
        if period == None:
            period = "hafta"
        if self.c.events == set():
            print("No events in calendar")
            return None
        else:
            event_list=[]
            now = pytz.utc.localize(datetime.now())
            if period == 'hafta':
                nextweek = now + relativedelta(weeks =+1)
            if period == 'ay':
                nextweek =now + relativedelta(months =+1)
            if period == 'tum':
                nextweek = now + relativedelta(years =+100)
            for event in self.c.events:
                event_date = event.begin.datetime
                if (event_date >= now) and (event_date <= nextweek):
                    event_list.append(event)
            return event_list

class Calendar_skill():
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.calendar=GladosCalendar()
        self.calendar.load()
        self.ai_listen = self.calendar.listen.Glados_listen
        self.ai_speak = GladosTTS.Gladostts
        self.aylar = ["ocak","şubat","mart","nisan","mayıs","haziran","temmuz","ağustos","eylül","ekim","kasım","aralık"]
        self.removable = ["saat","hour","minute","dakika"]
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    def calendar_parser(self,sentence_words):
        sentence_words = sentence_words
        count_wordindex = 0
        count_baglac = 0
        month_use = ""
        flag = False
        for i in sentence_words:
            word = i
            count = 0
            for i in self.aylar:
                if word == i :
                    month_use=self.months[count]
                    break
                count = count +1
            if len(month_use) == 0:
                count_wordindex = count_wordindex + 1
            else : 
                break
        sentence_words[count_wordindex] = month_use
        if "saat" in sentence_words:
            sentence_words.remove("saat")
        for i in sentence_words:
            new_word = ""
            if '.' in i :
                for a in i :
                    if a != '.':
                        new_word=new_word + a
                    elif a == '.':
                        new_word = new_word + ':'
                flag = True
            count_baglac = count_baglac + 1
            if flag == True :
                sentence_words[count_baglac-1] = new_word
                sentence_words = sentence_words[:count_baglac] 
                break

        return sentence_words
    def add_event(self)->bool:
        try:
            self.ai_speak("What is the name of the event?")
            event_name =self.ai_listen()
            self.ai_speak("When is this event?")
            event_begin = self.ai_listen()
            sentence_words = nltk.word_tokenize(event_begin)
            sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
            sentence_words=self.calendar_parser(sentence_words=sentence_words)
            
                
            event_begin = ' '.join([str(n) for n in sentence_words])
            print(event_begin)
            #event_isodate = dateparser.parse(event_begin).strftime("%Y-%m-%d %H:%M:%S")
            event_isodate=datetime.strptime(event_begin,"%d %B %Y %H:%M")
            self.ai_speak("What is the event description?")
            event_description = self.ai_listen()
            self.calendar.add_event(begin = event_isodate,name=event_name,description=event_description)
            self.calendar.save()
            return True
        except:
            print("error ")
            return False

    def remove_event(self)->bool:
        self.ai_speak("What is the name of the event you want to remove?")
        try:
            event_name = self.ai_listen()
            try:
                self.calendar.remove_event(event_name=event_name)
                self.ai_speak("Event removed successfully")
                self.calendar.save()
                return True
            except:
                self.ai_speak(f"Sorry I couldn't find the event {event_name}")
                return False
        except:
            return False

    def list_events(self,period):
        this_period = self.calendar.list_events(period=period)
        if this_period is not None :
            message = "There"
            if len(this_period) > 1:
                message = message + ' are '
            else : 
                message = message + ' is '
            message = message + str(len(this_period))
            if len(this_period) >1:
                message = message + ' events '
            else : 
                message = message + ' event '
            message = message + " in the diary "
            self.ai_speak(f"{message}")
            for event in this_period :
                event_date = event.begin.datetime
                weekday = datetime.strftime(event_date, "%A")
                day = str(event.begin.datetime.day)
                month = datetime.strftime(event_date,"%B")
                year = datetime.strftime(event_date,"%Y")
                time = datetime.strftime(event_date,"%I:%M %p")
                name = event.name
                description = event.description
                message = " On " + weekday + " " + day + " of " + month + " " + year + " at " + time
                message = message + ",there is an event called " + name
                message = message + " with an event description of "+ description
                self.ai_speak(f"{message}")
    def handle_command(self, command:str):
        
        if command in ['add event','add to calendar','new event','add a new event']:
            self.add_event()
        if command in ['delete event','remove event','cancel event']:
            self.remove_event()
        if command in ['list events',"what's on this month","what's coming up this month"]:
            self.list_events(period='this month')
        if command in ["what's on this week","what's coming up this week","what's happening"]:
            self.list_events(period='this week')
        if command in ['list all events']:
            self.list_events(period='all')


