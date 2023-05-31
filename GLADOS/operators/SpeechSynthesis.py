from ast import While
from itertools import count
import time
import torch
import matplotlib.pyplot as plt
import pathlib , os
from espnet2.bin.tts_inference import Text2Speech
from espnet2.utils.types import str_or_none
import scipy.io.wavfile
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition
from GladosAIModule import GladosAIModule
class GladosTTS:
    def Gladostts(x):
        #@title Choose English model { run: "auto" }
        lang = 'English'
        tag = 'kan-bayashi/ljspeech_vits' #@param ["kan-bayashi/ljspeech_tacotron2", "kan-bayashi/ljspeech_fastspeech", "kan-bayashi/ljspeech_fastspeech2", "kan-bayashi/ljspeech_conformer_fastspeech2", "kan-bayashi/ljspeech_vits"] {type:"string"}
        vocoder_tag = "none" #@param ["none", "parallel_wavegan/ljspeech_parallel_wavegan.v1", "parallel_wavegan/ljspeech_full_band_melgan.v2", "parallel_wavegan/ljspeech_multi_band_melgan.v2", "parallel_wavegan/ljspeech_hifigan.v1", "parallel_wavegan/ljspeech_style_melgan.v1"] {type:"string"}

        text2speech = Text2Speech.from_pretrained(
            model_tag=str_or_none(tag),
            vocoder_tag=str_or_none(vocoder_tag),
            device="cuda",
            # Only for Tacotron 2 & Transformer
            threshold=0.5,
            # Only for Tacotron 2
            minlenratio=0.0,
            maxlenratio=10.0,
            use_att_constraint=False,
            backward_window=1,
            forward_window=3,
            # Only for FastSpeech & FastSpeech2 & VITS
            speed_control_alpha=1.0,
            # Only for VITS
            noise_scale=0.667,
            noise_scale_dur=0.8,
        )

        # synthesis
        with torch.no_grad():
            start = time.time()
            wav = text2speech(x)["wav"]
        rtf = (time.time() - start) / (len(wav) / text2speech.fs)
        print(f"RTF = {rtf:5f}")
        # let us listen to generated samples
        wav_dosya=wav.view(-1).cpu().numpy()
        wav_dosya = (wav_dosya * (2 ** 15 - 1)).astype("<h")#Dosya tipi int16
        dtype=scipy.io.wavfile.write("audio_file.wav",text2speech.fs , wav_dosya)
        wav_file= AudioSegment.from_file(file="audio_file.wav",format="wav")
        play(wav_file)
        stop_condition = "-"
        return stop_condition
    
class GladosListen():
    def __init__(self):
        self.SpeechRecognizer = speech_recognition.Recognizer()
        self.GladosAI = GladosAIModule()
        #self.translationTable = str.maketrans("ğĞıİöÖüÜşŞçÇ", "gGiIoOuUsScC")
    #Modified listen function
    def Glados_listen(self,ai_response = True):
        with speech_recognition.Microphone() as mic:
                    self.SpeechRecognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    self.SpeechRecognizer.energy_threshold = 3000
                    audio = self.SpeechRecognizer.listen(mic)
                    period = ""
                    try:
                        inputted = self.SpeechRecognizer.recognize_google(audio,None,"tr-TR",show_all=False)
                        inputted = inputted.lower()
                        #inputted = inputted.translate(self.translationTable)
                        if ai_response:
                            ints=  self.GladosAI.predict_class(inputted)
                            if isinstance(ints,list): 
                                text = self.GladosAI.get_response(ints,self.GladosAI.intents)
                            else:
                                text = ints
                        else:
                            text = inputted
                        period_var = ["hafta","ay","tum"]
                        count = 0
                        for i in period_var:
                            if  period_var[count] in text:
                                period = period_var[count]
                            else:
                                period = "hafta"
                            count = count +1
                        print('{}'.format(text))
                    except speech_recognition.UnknownValueError:
                        print("Unknown Value")
                        text = "Unknown Value"
                        inputted = "Unknown Value"
                        self.SpeechRecognizer = speech_recognition.Recognizer()
                        time.sleep(1)
        if len(period) == 0:
            period = "hafta"
        return text,inputted,period      

class GladosListenWithoutAI():
    def __init__(self):
        self.SpeechRecognizer = speech_recognition.Recognizer()
    #Modified listen function
    def Glados_listen(self):
        while True:
            with speech_recognition.Microphone() as mic:
                        self.SpeechRecognizer.adjust_for_ambient_noise(mic, duration=0.2)
                        self.SpeechRecognizer.energy_threshold = 3000
                        audio = self.SpeechRecognizer.listen(mic)
                        try:
                            text = self.SpeechRecognizer.recognize_google(audio,None,"tr-TR",show_all=False)
                            text = text.lower()
                            print('{}'.format(text))
                        except speech_recognition.UnknownValueError:
                            print("Unknown Value")
                            text = "Unknown Value"
                            self.SpeechRecognizer = speech_recognition.Recognizer()
                            time.sleep(1)
            if text == 'Unknown Value':
                continue
            else : 
                break
        return text            