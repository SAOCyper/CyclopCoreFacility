import speech_recognition , time , os , logging,random , serial , pathlib ,Spotifyglados,cv2,socket,factory , loader,json,pickle , threading , sqlalchemy as db,imutils , struct,pygame
from GladosSoundLibrary import GladosSound
from Gladosnetflix import GladosNetflix
from GladosCalendar import Calendar_skill
from todo import GladosTodo
from Spotifyglados import SpotifyGlados
from SpotifyWebGlados import *
from PersonAdder import Adder
from GladosAIModule import GladosAIModule
from WeatherForecastGlados import Weather_skill
from dotenv import load_dotenv
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData, Table ,text
from SpeechSynthesis import GladosTTS,GladosListen
from UpdateAI import UpdateAI
from  Security_Camera.CyclopNotifications import Notification
from Security_Camera.CyclopNotificationSender import *
from Security_Camera.Security_Config import Configuration
from Gladoswikipedia import Glados_knowlodge
###Global text previous stored
text_before_before = None
text_before = None
#Decorator function for wakeup word
wakeup_word = "hello"
def listen_for_wakeup_word(func):
  def wrapper():
    global wakeup_word
    # Initialize the speech recognition engine
    r = speech_recognition.Recognizer()

    # Start listening for the wake-up word
    with speech_recognition.Microphone() as source:
      print("Listening for wake-up word...")
      audio = r.listen(source)

    # Try to recognize the wake-up word
    try:
      spoken_text = r.recognize_google(audio)
      spoken_text = spoken_text.lower()
      print(spoken_text)
      if spoken_text == wakeup_word:
        print("Wake-up word recognized:", spoken_text)
        return func()
      else:
        print("Speech not recognized as wake-up word")
        return
    except speech_recognition.UnknownValueError:
      print("Speech not recognized")
      return

  return wrapper
frame = 0
def camera_comm():
    global frame
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 
    camera_host = IPAddr
    camera_port = 15200
    client_socket_camera = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket_camera.connect((camera_host, camera_port))  # connect to the server

    client_socket_camera1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket_camera1.connect((camera_host, camera_port+1))  # connect to the server
    client_socket_camera2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket_camera2.connect((camera_host, camera_port+2))  # connect to the server
    client_socket_camera3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket_camera3.connect((camera_host, camera_port+3))  # connect to the server
    client_socket_camera4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket_camera4.connect((camera_host, camera_port+4))  # connect to the server

    while True:
        """ tx_data = pickle.dumps(tx_data)
        client_socket_camera.send(tx_data)  # send message
        received_response = client_socket_camera.recv(2048)
        received_response = pickle.loads(received_response) """
        #frame = imutils.resize(frame,width=640,height=480)
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        client_socket_camera.sendall(message)
        client_socket_camera1.sendall(message)
        client_socket_camera2.sendall(message)
        client_socket_camera3.sendall(message)
        client_socket_camera4.sendall(message)
class ArduinoCommuniction():
    def __init__(self):
        self.arduino = serial.Serial(port="com4", baudrate=9600, timeout=.1)#port number = COM'N' -----> N-1
    
    def arduino_send():
        pass
    def arduino_read():
        pass

class Glados_OS:
    
    def __init__(self,initial):
        path_parent = os.path.dirname(os.getcwd())
        engine = db.create_engine('sqlite:///'+ path_parent + "\Operation_Glados\GLADOS\operators\website\database.db")
        result1 = engine.execute(text("SELECT data FROM spotify_username"))
        result2 = engine.execute(text("SELECT data FROM spotify_email"))
        result3 = engine.execute(text("SELECT data FROM spotify_password"))
        result4 = engine.execute(text("SELECT data FROM netflix_email"))
        result5 = engine.execute(text("SELECT data FROM netflix_password"))
        print(f"Selected {result1.rowcount} rows.")
        for row in result1.fetchall():
            self.spotify_username = row['data']
        for row in result2.fetchall():
            self.spotify_email = row['data']
        for row in result3.fetchall():
            self.spotify_password = row['data']
        for row in result4.fetchall():
            self.netflix_email = row['data']
        for row in result5.fetchall():
            self.netflix_password = row['data']
        load_dotenv('.env')
        self.initial = initial
        self.camera_condition = False
        self.clientadder = Adder()
        self.spotifywebapi = SpotifyWebAPI(login_id=self.spotify_email,password=self.spotify_password)
        self.spotify = SpotifyGlados(self.spotify_username)
        self.listen = GladosListen()
        self.calendar = Calendar_skill()
        self.todo = GladosTodo()
        self.ai = UpdateAI()
        self.config = Configuration()
        self.camera = VideoCamera(self.config)
        self.arduino = None
        cam_comm_thread = threading.Thread(target=camera_comm)
        cam_comm_thread.start()
        self.wiki = Glados_knowlodge()
        #self.arduino = ArduinoCommuniction()
        #self.translationTable = str.maketrans("ğĞıİöÖüÜşŞçÇ", "gGiIoOuUsScC")
        #self.GladosAI = GladosAIModule()

    def Camera(self):
        global frame
        
        self.path=pathlib.Path(__file__).parent.resolve()
        os.chdir(self.path)
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        stop_condition="empty"
        stopBit = "empty"
        leftcounter=0
        rightcounter=0
        stopcounter=0
        findcounter=0
        self.trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("face-trainner.yml")
        self.labels = {"person_name": 1}
        with open("labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            self.labels = {v:k for k,v in og_labels.items()}
        if self.arduino != None:
            if not self.arduino.isOpen():
                self.arduino.open()
                print('com4 is open', self.arduino.isOpen())
        while self.camera_condition :
                # Capture frame-by-frame
                
                ret, frame = self.cap.read()
                rows,cols,_ =frame.shape
                
                xmedium = int(cols/2)
                y_medium = int(rows/2)
                horizontalboundary1 =int((xmedium/25)*20)
                horizontalboundaryvar = int(xmedium - horizontalboundary1)
                horizontalboundary2 = int(xmedium + horizontalboundaryvar)
                verticalboundary1=int((y_medium/2))
                verticalboundary3=int((y_medium/4))
                verticalboundary4=int((y_medium*2))-verticalboundary3
                verticalboundary2=y_medium+verticalboundary1
                gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
                faces = self.trained_face_data.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=4)
                if len(faces)>0:
                    for (x, y, w, h) in faces:
                        #print(x,y,w,h)
                        roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
                        roi_color = frame[y:y+h, x:x+w]

                        # recognize? deep learned model predict keras tensorflow pytorch scikit learn
                        id_, conf = self.recognizer.predict(roi_gray)
                        if conf>=4 or conf <= 85:
                            #print(5: #id_)
                            #print(labels[id_])
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            name = self.labels[id_]
                            color = (255, 255, 255)
                            stroke = 2
                            
                            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                        yatay=int((x+x+w)/2)
                        dikey=int((y+y+h)/2)
                        color = (255, 0, 0) #BGR 0-255 
                        stroke = 2
                        end_cord_x = x + w
                        end_cord_y = y + h
                        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
                        if verticalboundary3<dikey<verticalboundary1:
                                print("Upx1")
                                num = "u"
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline()  
                                    string= data.decode()
                                    stripped = string.strip()
                                    print(stripped)
                                
                        if verticalboundary1<dikey<verticalboundary2:
                                print("Vertical stopped")
                                num = "m"
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline()  
                                
                        if verticalboundary2< dikey <verticalboundary4 :
                                print("Downx1")
                                num = "d"
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline()
                                    string= data.decode()
                                    stripped = string.strip()
                                    print(stripped)
                        if 0<yatay<horizontalboundary1:
                            print("Left")
                            num = "l"
                            rightcounter=0
                            findcounter=0
                            stopcounter=0
                            leftcounter = leftcounter +1
                            if leftcounter<2:
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline() 
                                    string= data.decode()
                                    stripped = string.strip()
                                    print(stripped)
                                    #arduino.write(bytes(stop_condition, 'utf-8'))
                                    leftcounter=0
                            
                            break    
                        if horizontalboundary2<yatay<640 :  
                            print("Right") 
                            num = "r"
                            leftcounter=0
                            findcounter=0
                            stopcounter=0
                            rightcounter = rightcounter+1
                            if rightcounter <2:
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline()
                                    string= data.decode()
                                    stripped = string.strip()
                                    print(stripped) 
                                    #arduino.write(bytes(stop_condition, 'utf-8'))
                                    rightcounter=0
                            break
                        if horizontalboundary1<yatay or yatay<horizontalboundary2:
                            print("Stopped")
                            num = "Z"
                            leftcounter=0
                            findcounter=0
                            rightcounter=0
                            stopcounter = stopcounter +1
                            if self.arduino != None:
                                self.arduino.write(bytes(num, 'utf-8'))
                                data = self.arduino.readline()
                            break    
                           
                else:
                    print("Search")
                    num = "F"
                    leftcounter=0
                    rightcounter=0
                    stopcounter=0
                    findcounter = findcounter +1
                    if findcounter <2 and stopBit != "angle <6":
                        if self.arduino != None:
                            self.arduino.write(bytes(num, 'utf-8'))
                            time.sleep(0.001)
                            data = self.arduino.readline()
                            string= data.decode()
                            stripped = string.strip()
                            stop_condition = stripped
                            if stop_condition == "angle <6":
                                stopBit=stop_condition
                            print(stripped)
                            findcounter=0
                    if stopBit == "angle <6":
                        find1="G"
                        if self.arduino != None:
                            self.arduino.write(bytes(find1, 'utf-8'))
                            time.sleep(0.001)
                            data = self.arduino.readline()
                            string= data.decode()
                            stripped = string.strip()
                            stop_condition = stripped
                            print(stripped)
                            if stop_condition== "angle > 350":
                                stopBit = "empty"
                                break
                    
                    
                # Display the resulting frame
                cv2.imshow('frame',frame)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    print("....RESETTING CAMERA....")
                    num = "S"
                    if self.arduino != None:
                        self.arduino.write(bytes(num, 'utf-8'))
                        time.sleep(0.5)
                        data = self.arduino.readline()
                        string= data.decode()
                        stripped = string.strip()
                        print(stripped)
                        self.arduino.close()
                    break
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()


    def Glados_run(self):
        global text_before_before , text_before
        path=pathlib.Path(__file__).parent.resolve()
        os.chdir(path) 
        takip_count = 0
        get_previous = True
        while self.initial:
            """ if not self.arduino.isOpen():
                self.arduino.open()
                print('com4 is open', self.arduino.isOpen()) """
            text,inputted,period=self.listen.Glados_listen(True)
            
            ########################################
            ######Modified Skill Selection##########
            ########################################
            """ if text:
                print(f"command heard: {text}")
                for skill in self.skills:
                    if text in self.skills.commands(text):
                        skill.handle_command(text ,ai_listen=Glados_OS.Glados_listen,ai_say=GladosTTS.Gladostts) """
                        
            ########################################
            ########################################
            ########################################
            if text == 'sistemi kapat':
                print("Glados Closed")
                num = "C"
                if self.arduino != None:
                    self.arduino.write(bytes(num, 'utf-8'))
                    time.sleep(0.01)
                    data = self.arduino.readline() 
                    string= data.decode()
                    stripped = string.strip()
                    print(stripped)
                #GladosSound.soundlibrary(text) 
                GladosTTS.Gladostts("Turning off the system")
                self.initial = False
                return self.initial
            elif text == 'sistemi aç' or text == 'sistemi başlat':
                print("Glados Initialized")
                num = "O"
                if self.arduino != None:
                    self.arduino.write(bytes(num, 'utf-8'))
                    time.sleep(0.01)
                    data = self.arduino.readline() 
                    string= data.decode()
                    stripped = string.strip()
                    print(stripped)
                #GladosSound.soundlibrary(text)   
                GladosTTS.Gladostts("System is operating now")
            elif text == 'netflix aç':
                
                GladosTTS.Gladostts("Netflix is opening")
                run=GladosNetflix(self.netflix_email,self.netflix_password,"Kengan Ashura")
                run.Glados_netflix() 
            elif text == 'spotify aç':
                self.spotify.Glados_spotify(text)
                #self.spotifywebapi.SpotifyWebGlados()
            elif text == 'ışıkları aç' or text == 'ışıkları yak':
                print("Lights mode 1 is on")
                num = "L"
                if self.arduino != None:
                    self.arduino.write(bytes(num, 'utf-8'))
                    time.sleep(0.01)
                    data = self.arduino.readline() 
                    string= data.decode()
                    stripped = string.strip()
                    print(stripped)
                #GladosSound.soundlibrary(text) 
                GladosTTS.Gladostts("Light mode 1 is activated")
            elif text == 'güçlü ışıkları aç' or text == 'ışıkları güçlendir':
                print("Lights mode 2 is on")
                num = "H"
                if self.arduino != None:
                    self.arduino.write(bytes(num, 'utf-8'))
                    time.sleep(0.01)
                    data = self.arduino.readline() 
                    string= data.decode()
                    stripped = string.strip()
                    print(stripped)
                #GladosSound.soundlibrary(text) 
                GladosTTS.Gladostts("Light mode 2 is activated")    
            elif text == 'yeni kişi tanımla':
                #GladosSound.soundlibrary(text)
                GladosTTS.Gladostts("Starting to register new identity.")
                self.clientadder.PersonAdder()
            elif text == 'kimliği kaydet':    
                #GladosSound.soundlibrary(text)
                self.name=self.clientadder.PersonRecognizer()
                GladosTTS.Gladostts("New identity is now registered to system.Welcome {}".format(self.name))
            elif 'takip' in text:
                #GladosCamera.Camera(self)
                GladosTTS.Gladostts("Tracking is started")
                if takip_count == 0:
                    self.camera_condition  = True
                    camera_thread = threading.Thread(target = self.camera.Glados_detect())
                    camera_thread.start()
                    takip_count += 1 
                else:
                    self.camera_condition = False
                    takip_count = 0
                
            elif text == 'hava durumu nasıl' : 
                word ="city choice"
                Weather_skill.handle_command()
            elif text == "random konışma yap":
                num = "p"
                if self.arduino != None:
                    self.arduino.write(bytes(num, 'utf-8'))
                    time.sleep(0.1)
                    data = self.arduino.readline() 
                    string= data.decode()
                    stripped = string.strip()
                    print(stripped)
                    stop_condition=GladosTTS.Gladostts("The inspiration for the character's creation extends from Wolpaw's use of a text-to-speech program while writing lines for the video game Psychonauts. Other game developers working on Psychonauts found the lines funnier as a result of the synthesized voice. ")
                    self.arduino.write(bytes(stop_condition, 'utf-8'))
                    time.sleep(0.1)
                    data = self.arduino.readline() 
                    string= data.decode()
                    stripped = string.strip()
                    print(stripped)
            elif text == "takvime etkinlik ekle":
                self.calendar.add_event()
            elif text == "takvimden etkinlik çıkar":
                self.calendar.remove_event()
            elif text == "takvimde bu haftayi göster":
                period = "hafta"
                self.calendar.list_events(period=period)
            elif text == "bu ayki takvimi göster":
                period = "ay"
                self.calendar.list_events(period=period)
            elif text == "tüm etkinlikleri göster":
                period = "tüm"
                self.calendar.list_events(period=period)
            elif text == "yapılacaklar listesine ekle":
                self.todo.add_todo()
            elif text == "yapılacaklar listesinden çıkar":
                self.todo.remove_todo()
            elif text == "yapılacaklar listesini aç":
                self.todo.list_todos()
            elif text == "Unknown Value":
                continue 
            elif text == "cevabı kaydet":
                get_previous = False
                ###cevabı öğren
                GladosTTS.Gladostts("Please tell answer to be learned")
                text,inputted,period=self.listen.Glados_listen(False)
                self.ai.learn_new_response(inputted,text_before)
                #UpdateAI.learn(inputted,text_before)
                text_before = None
                pass
            elif text == "Unknown":
                GladosTTS.Gladostts("I couldn't understand the command.What can I do for you?")
                self.initial = True 
            else :
                
                text = ['plus' if '+'in s else s for s in text]
                text = ['minus' if '-'in s else s for s in text]
                text = ['times ' if '*'in s else s for s in text]
                text = ['divided by' if '/'in s else s for s in text]
                text = ['power of' if '^'in s else s for s in text]
                text = ['eşittir' if '='in s else s for s in text]
                text = ''.join(str(x) for x in text)
                print(text)
                GladosTTS.Gladostts(text)
                self.initial = True
            if get_previous :
                text_before = inputted
                get_previous = True 


class VideoCamera(Glados_OS):
    binary = True
    def __init__(self, config):
        self.config = config
        self.video = cv2.VideoCapture(int(self.config.get('Video')['camera']))
        self.videoWriter = None
        self.online = False
        self.recording = False
        self.first_captured = None
        self.notification = Notification(config) if config.is_exist('Notifications', 'pushover') else None
        
    def __del__(self):
        self.video.release()
        
    def finished(self):
        self.video.release()
        self.notification.release()

    def start(self,sens, method, mail, sound, notif):
        self.online = False
        logging.info('Active security started at ' + str(datetime.datetime.now()))
        iterator = 0
        repeated = 0
        sequence_capture = False
        self.first_captured = None
        while True:
            success, image = self.video.read()
            if not success:
                continue
            iterator += 1
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            if method == 'face':
                faceCascade = cv2.CascadeClassifier("haarcascade/faceDetect.xml")
            #elif method == 'ubody':
                #faceCascade = cv2.CascadeClassifier("haarcascade/haarcascade_upperbody.xml")
            elif method == 'fbody':
                faceCascade = cv2.CascadeClassifier("haarcascade/haarcascade_fullbody.xml")
            elif method == 'move':
                if self.first_captured is None:
                    self.first_captured = gray
                frameDelta = cv2.absdiff(self.first_captured, gray)
                self.first_captured = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for c in cnts:
                    if cv2.contourArea(c) < int(self.config.get('Video')['min_movement_object']):
                        continue
                    repeated += 1
                    break
            if method == 'ubody' or method == 'fbody' or method == 'face':
                #TODO export arguments to config file
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    flags=0)
                if type(faces) is not tuple:
                    if sequence_capture:
                        repeated += 1
                    sequence_capture = True
                else:
                    sequence_capture = False
                    repeated = 0
            if self.online:
                logging.info('Active security Stopped by user at ' + str(datetime.datetime.now()))
                self.first_captured = None
                return
            if repeated == (6 - sens):
                logging.info('Figure has been Detected at ' + str(datetime.datetime.now()))
                ret, jpeg = cv2.imencode('.jpg', image)
                img = jpeg.tostring()
                if notif:
                    try:
                        logging.info('Sending notification  ' + str(datetime.datetime.now()))
                        if 'bxc' in self.config.get("Notifications"):
                            send_notification(self.config)
                        if self.notification.user:
                            self.notification.send_notification()
                    except:
                        logging.warn('Error sending notification  ' + str(datetime.datetime.now()))
                if sound: 
                    pygame.mixer.music.load(self.config.get('Sound')['alarm'])
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() == True:
                        continue

                if mail:
                    try:
                        logging.info('Sending email ' + str(datetime.datetime.now()))
                        sendMessage(img, self.config)
                    except:
                        logging.info('Error Sending Mail ' + str(datetime.datetime.now()))
                self.first_captured = None
                return
            if iterator == 10:
                iterator = 0
                repeated = 0

    def record(self,upload, cloud):
        self.recording = True
        logging.info('Video recording started at ' + str(datetime.datetime.now()))
        timestr = time.strftime("%Y%m%d-%H%M%S")
        videoWriter = cv2.VideoWriter(self.config.get('File')['videos'] + 'video' + timestr + ".avi", cv2.cv.CV_FOURCC('M','J','P','G'), int(self.config.get('Video')['fps']),
               (640,480))
        while self.recording:
            while True:
                success, image = self.video.read()
                if not success:
                    continue
                else:
                    break
            if self.recording:
                videoWriter.write(image)
                time.sleep(0.08)
        videoWriter.release()
        if upload:
            f = open(self.config.get('File')['videos'] + 'video' + timestr + ".avi", 'rb')
            data = f.read()
            #cloud.upload_file(data, '/video' + timestr + ".avi")

    def playAudio(self, time):
        pygame.mixer.music.load("audio" + time + ".wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def endVideo(self):
        self.recording = False

    def get_frame(self, faced,saved =False, video=False, videoStop=False):
        while True:
            success, image = self.video.read()
            if not success:
                continue
            else:
                break
        if video:
            cv2.circle(image,(100, 20), 15, (0, 0, 255), -1)
        if faced:
            faceCascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                flags=0)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            ret, jpeg = cv2.imencode('.jpg', image)
            return (jpeg.tostring())
        ret, jpeg = cv2.imencode('.jpg', image)
        return (jpeg.tostring())
    
    def Glados_detect(self):
        global frame
        self.path=pathlib.Path(__file__).parent.resolve()
        os.chdir(self.path)
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        stop_condition="empty"
        stopBit = "empty"
        leftcounter=0
        rightcounter=0
        stopcounter=0
        findcounter=0
        self.trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("face-trainner.yml")
        self.labels = {"person_name": 1}
        with open("labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            self.labels = {v:k for k,v in og_labels.items()}
        if self.arduino != None:
            if not self.arduino.isOpen():
                self.arduino.open()
                print('com4 is open', self.arduino.isOpen())
        while self.camera_condition :
                # Capture frame-by-frame
                
                ret, frame = self.cap.read()
                rows,cols,_ =frame.shape
                
                xmedium = int(cols/2)
                y_medium = int(rows/2)
                horizontalboundary1 =int((xmedium/25)*20)
                horizontalboundaryvar = int(xmedium - horizontalboundary1)
                horizontalboundary2 = int(xmedium + horizontalboundaryvar)
                verticalboundary1=int((y_medium/2))
                verticalboundary3=int((y_medium/4))
                verticalboundary4=int((y_medium*2))-verticalboundary3
                verticalboundary2=y_medium+verticalboundary1
                gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
                faces = self.trained_face_data.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=4)
                if len(faces)>0:
                    for (x, y, w, h) in faces:
                        #print(x,y,w,h)
                        roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
                        roi_color = frame[y:y+h, x:x+w]

                        # recognize? deep learned model predict keras tensorflow pytorch scikit learn
                        id_, conf = self.recognizer.predict(roi_gray)
                        if conf>=4 or conf <= 85:
                            #print(5: #id_)
                            #print(labels[id_])
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            name = self.labels[id_]
                            color = (255, 255, 255)
                            stroke = 2
                            
                            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                        yatay=int((x+x+w)/2)
                        dikey=int((y+y+h)/2)
                        color = (255, 0, 0) #BGR 0-255 
                        stroke = 2
                        end_cord_x = x + w
                        end_cord_y = y + h
                        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
                        if verticalboundary3<dikey<verticalboundary1:
                                print("Upx1")
                                num = "u"
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline()  
                                    string= data.decode()
                                    stripped = string.strip()
                                    print(stripped)
                                
                        if verticalboundary1<dikey<verticalboundary2:
                                print("Vertical stopped")
                                num = "m"
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline()  
                                
                        if verticalboundary2< dikey <verticalboundary4 :
                                print("Downx1")
                                num = "d"
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline()
                                    string= data.decode()
                                    stripped = string.strip()
                                    print(stripped)
                        if 0<yatay<horizontalboundary1:
                            print("Left")
                            num = "l"
                            rightcounter=0
                            findcounter=0
                            stopcounter=0
                            leftcounter = leftcounter +1
                            if leftcounter<2:
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline() 
                                    string= data.decode()
                                    stripped = string.strip()
                                    print(stripped)
                                    #arduino.write(bytes(stop_condition, 'utf-8'))
                                    leftcounter=0
                            
                            break    
                        if horizontalboundary2<yatay<640 :  
                            print("Right") 
                            num = "r"
                            leftcounter=0
                            findcounter=0
                            stopcounter=0
                            rightcounter = rightcounter+1
                            if rightcounter <2:
                                if self.arduino != None:
                                    self.arduino.write(bytes(num, 'utf-8'))
                                    data = self.arduino.readline()
                                    string= data.decode()
                                    stripped = string.strip()
                                    print(stripped) 
                                    #arduino.write(bytes(stop_condition, 'utf-8'))
                                    rightcounter=0
                            break
                        if horizontalboundary1<yatay or yatay<horizontalboundary2:
                            print("Stopped")
                            num = "Z"
                            leftcounter=0
                            findcounter=0
                            rightcounter=0
                            stopcounter = stopcounter +1
                            if self.arduino != None:
                                self.arduino.write(bytes(num, 'utf-8'))
                                data = self.arduino.readline()
                            break    
                           
                else:
                    print("Search")
                    num = "F"
                    leftcounter=0
                    rightcounter=0
                    stopcounter=0
                    findcounter = findcounter +1
                    if findcounter <2 and stopBit != "angle <6":
                        if self.arduino != None:
                            self.arduino.write(bytes(num, 'utf-8'))
                            time.sleep(0.001)
                            data = self.arduino.readline()
                            string= data.decode()
                            stripped = string.strip()
                            stop_condition = stripped
                            if stop_condition == "angle <6":
                                stopBit=stop_condition
                            print(stripped)
                            findcounter=0
                    if stopBit == "angle <6":
                        find1="G"
                        if self.arduino != None:
                            self.arduino.write(bytes(find1, 'utf-8'))
                            time.sleep(0.001)
                            data = self.arduino.readline()
                            string= data.decode()
                            stripped = string.strip()
                            stop_condition = stripped
                            print(stripped)
                            if stop_condition== "angle > 350":
                                stopBit = "empty"
                                break
                    
                    
                # Display the resulting frame
                cv2.imshow('frame',frame)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    print("....RESETTING CAMERA....")
                    num = "S"
                    if self.arduino != None:
                        self.arduino.write(bytes(num, 'utf-8'))
                        time.sleep(0.5)
                        data = self.arduino.readline()
                        string= data.decode()
                        stripped = string.strip()
                        print(stripped)
                        self.arduino.close()
                    break
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

logging.basicConfig(filename='app.log',level=logging.DEBUG)
pygame.mixer.init()

@listen_for_wakeup_word
def start_cyclop():
    madeliane = Glados_OS(True)
    madeliane.Glados_run()

#arduino = serial.Serial(port="com4", baudrate=9600, timeout=.1)#port number = COM'N' -----> N-1

""" if __name__ == "__main__":
    while True:
        if arduino.in_waiting > 0 :
            condition_fullfilled = True
            trigger = arduino.read()
            if trigger == b"1":
                wakeup_word_detected = listen_for_wakeup_word(wakeup_word)
                if wakeup_word_detected:
                    start_cyclop()
                else : 
                    time.sleep(1) """

madeliane = Glados_OS(True)
madeliane.Glados_run()
