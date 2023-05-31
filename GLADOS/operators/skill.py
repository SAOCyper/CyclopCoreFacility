from typing import Protocol
from SpeechSynthesis import GladosTTS,GladosListen

class Skill(Protocol):

    def commands(self, command:str):
        """ Return a list of commands that this skill can handle """
        pass

    def handle_command(self, command:str, ai_listen:GladosListen.Glados_listen,ai_say=GladosTTS.Gladostts):
        """ Handle a command """
        pass