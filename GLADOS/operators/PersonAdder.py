import cv2
import os
from GladosSoundLibrary import GladosSound
import speech_recognition
import time
from Faces_train import Glados_MachineLearn
import pathlib
import factory
from SpeechSynthesis import GladosListenWithoutAI
from dataclasses import dataclass
class Adder:
    def __init__(self):
        self.ClientFaceStructure = Glados_MachineLearn()
        self.directory=pathlib.Path(__file__).parent.resolve()
        self.listen=GladosListenWithoutAI()
        self.listen = self.listen.Glados_listen
        os.chdir(self.directory)
        self.trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
       
    def PersonAdder(self):
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        os.chdir(path_parent + r'\images')
        cap = cv2.VideoCapture(0)
        while True:
            _,frame = cap.read()
            faces = self.trained_face_data.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=4)
            #cv2.imshow("Frame",frame)
            #cv2.waitKey(0)
            if len(faces)>0:
                """ recognizer = speech_recognition.Recognizer() """
                name=self.listen()
                name.replace(" ", "_")
                new_path = self.directory+"\{}".format(name)
                print(new_path)
                filename= name + ".jpeg" 
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                break
        directory = new_path
        os.chdir(directory)
        cv2.imwrite(filename,frame)
        cap.release()    
    def PersonRecognizer(self):
        os.chdir(self.directory)
        text = 'Kayıt olacak kullanıcı '
        GladosSound.soundlibrary(text)
        """ recognizer = speech_recognition.Recognizer() """
        name = self.listen()
        obj = Glados_MachineLearn()
        name=obj.face_train()
        return name


