from pathlib import Path
import pyaudio
import wave
import os
import pathlib
from speech_recognition import UnknownValueError

class GladosSound():
    

    def soundlibrary(text):
            
            commands = {'sistemi aktifleştir' : "All_systems_are_online.wav",
                      'sistemi başlat' : "All_systems_are_online.wav",
                      'sistemi aktive et' : "All_systems_are_online.wav",
                      'sistemi aç' : "All_systems_are_online.wav",
                      'sistemi çalıştır' : "All_systems_are_online.wav",
                      'kimliği kaydet' : "New_identity_is_now_registered.wav",
                      'yeni kimlik kaydet' : "New_identity_is_now_registered.wav",
                      'kişinin kimliğini kaydet' : "New_identity_is_now_registered.wav",
                      'yeni kişi tanımla' : "Recognize_in_process.wav",
                      'yeni kullanıcı tanımla' : "Recognize_in_process.wav",
                      'yeni kişiyi tanı' : "Recognize_in_process.wav",
                      'Google aç' : "WebsiteGoogle.wav",
                      'Google bağlan' : "WebsiteGoogle.wav",
                      'ışıkları aç' : "Permission_has_been_granted.wav",
                      'ışıkları söndür' : "Permission_has_been_granted.wav",
                      'ışıkları yak' : "Permission_has_been_granted.wav",
                      'kişi kontrolü' : "are_you_still_there.wav",
                      'kişi ismi al' : "please_say_your_name.wav",
                      'kişi sisteme kayıtlı mı bak' : "checking_records_of_authorized_person.wav",
                      'sistemi kapat':"Turning_off_the_system.wav"
                    }
            
            numbers = { '0':"0.vaw",'1':"1.vaw",'2':"2.vaw",'3':"3.vaw",'4':"4.vaw",
                        '5':"5.vaw",'6':"6.vaw",'7':"7.vaw",'8':"8.vaw",'9':"9.vaw",
                        '10':"10.vaw",'11':"11.vaw",'12':"12.vaw",'13':"13.vaw",'14':"14.vaw",
                        '15':"15.vaw",'16':"16.vaw",'17':"17.vaw",'18':"18.vaw",'19':"19.vaw",
                        '20':"20.vaw",'21':"21.vaw",'22':"22.vaw",'23':"23.vaw",'24':"24.vaw",
                        '25':"25.vaw",'26':"26.vaw",'27':"27.vaw",'28':"28.vaw",'29':"29.vaw",
                        '30':"30.vaw",'31':"31.vaw",'32':"32.vaw",'33':"33.vaw",'34':"34.vaw",
                        '35':"35.vaw",'36':"36.vaw",'37':"37.vaw",'38':"38.vaw",'39':"39.vaw",
                        '40':"40.vaw",'41':"41.vaw",'42':"42.vaw",'43':"43.vaw",'44':"44.vaw",
                        '45':"45.vaw",'46':"46.vaw",'47':"47.vaw",'48':"48.vaw",'49':"49.vaw",
                        '50':"50.vaw",'51':"51.vaw",'52':"52.vaw",'53':"53.vaw",'54':"54.vaw",
                        '55':"55.vaw",'56':"56.vaw",'57':"57.vaw",'58':"58.vaw",'59':"59.vaw",
                        '60':"60.vaw",'61':"61.vaw",'62':"62.vaw",'63':"63.vaw",'64':"64.vaw",
                        '65':"65.vaw",'66':"66.vaw",'67':"67.vaw",'68':"68.vaw",'69':"69.vaw",
                        '70':"70.vaw",'71':"71.vaw",'72':"72.vaw",'73':"73.vaw",'74':"74.vaw",
                        '75':"75.vaw",'76':"76.vaw",'77':"77.vaw",'78':"78.vaw",'79':"79.vaw",
                        '80':"80.vaw",'81':"81.vaw",'82':"82.vaw",'83':"83.vaw",'84':"84.vaw",
                        '85':"85.vaw",'86':"86.vaw",'87':"87.vaw",'88':"88.vaw",'89':"89.vaw",
                        '90':"90.vaw",'91':"91.vaw",'92':"92.vaw",'93':"93.vaw",'94':"94.vaw",
                        '95':"95.vaw",'96':"96.vaw",'97':"97.vaw",'98':"98.vaw",'99':"99.vaw",
                        '100':"0.vaw",}
            weather ={'hava durumu nasıl' : "WeatherReportİnitial.wav",
                      'parçalı güneşli' : "PartlySunny.wav",
                      'parçalı bulutlu' : "PartlyCloudy.wav",
                      'yağmurlu' : "Rainy.wav",
                      'Güneşli' : "Sunny.wav",
                      'karlı' : "Snowy.wav",
                      'city choice':"city_choice.wav",
                      'humidity ':"Humidity_is.wav",
                      'Max_degree':"maximumdegree.wav",
                      'Min_degree':"minimumdegree.wav",
                      'weather_condition':"weathercondition.wav",
                      }
            spotify = {'şarkı 1' : "Defective.wav",
                     'şarkı 2' : "If_ı_were_a_core.wav",
                     'şarkı 3' : "Turret_anthem.wav",
                     'şarkı 4' : "Carrol_of_the_bells.wav",
                     'şarkı 5' : "I_dont_say_goodbye.wav",
                     'artist seçildi' : "Artist_name_has_been_acquired.wav",
                     'Spotify kapatılıyor' : "Closing_spotify.wav",
                     'Sanatçı değiştiriliyor' : "Looking_for_new_artist.wav",
                     'Şarkı seçildi' : "Song_selection_has_been_acquired.wav",
                     'Artist seçimi beklemede' : "Specify_artist_name.wav",
                     'Şarkı seçimi beklemede' : "Specify_song_name.wav",
                     'spotify ac' : "Starting_spotify.wav",
                    } 
            os.chdir(pathlib.Path(__file__).parent.resolve()) # Get the current working directory
            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)
            sound_path = path_parent + r'\sounds\wav'
            os.chdir(sound_path)
            if text in commands:
                path = os.getcwd()
                if path !=sound_path + r'\General_wav':
                    SOUND_DIR= sound_path + r'\General_wav'
                    path = SOUND_DIR
                    os.chdir(SOUND_DIR)
                value = commands.get(text)
                item = r'\{}'.format(value)
                output = path + item
                wf = wave.open(output, 'rb')
                p = pyaudio.PyAudio()
                def callback(in_data, frame_count, time_info, status):
                    data = wf.readframes(frame_count)
                    return (data, pyaudio.paContinue)
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True,stream_callback=callback)
                # start the stream
                stream.start_stream() 
            elif text in weather:
                path = os.getcwd()
                if path !=sound_path + r'\Weather_wav':
                    SOUND_DIR=sound_path + r'\Weather_wav'
                    path = SOUND_DIR
                    os.chdir(SOUND_DIR)
                value = weather.get(text)
                item = r'\{}'.format(value)
                output = path + item
                wf = wave.open(output, 'rb')
                p = pyaudio.PyAudio()
                def callback(in_data, frame_count, time_info, status):
                    data = wf.readframes(frame_count)
                    return (data, pyaudio.paContinue)
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True,stream_callback=callback)
                    # start the stream
                stream.start_stream() 
            elif text in spotify:
                path = os.getcwd()
                if path != sound_path + r'\Spotify_wav':
                    SOUND_DIR=sound_path + r'\Spotify_wav'
                    path = SOUND_DIR
                    os.chdir(SOUND_DIR)
                
                value = spotify.get(text)
                item = r'\{}'.format(value)
                output = path + item
                wf = wave.open(output, 'rb')
                p = pyaudio.PyAudio()
                def callback(in_data, frame_count, time_info, status):
                    data = wf.readframes(frame_count)
                    return (data, pyaudio.paContinue)
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True,stream_callback=callback)
                # start the stream
                stream.start_stream() 
            elif text in numbers:
                path = os.getcwd()
                if path != sound_path + r'\0_to_100_wav':
                    SOUND_DIR= sound_path + r'\0_to_100_wav'
                    path = SOUND_DIR
                    os.chdir(SOUND_DIR)
                value = numbers.get(text)
                item = '\{}'.format(value)
                output = path + item
                #playsound(output)
                wf = wave.open(output, 'rb')
                p = pyaudio.PyAudio()
                def callback(in_data, frame_count, time_info, status):
                    data = wf.readframes(frame_count)
                    return (data, pyaudio.paContinue)
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True,stream_callback=callback)
                # start the stream
                stream.start_stream() 
                
                    
                
                