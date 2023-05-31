from hashlib import new
from PyQt5 import uic
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog , QVBoxLayout , QWidget , QSizePolicy,QPlainTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer, QDateTime, Qt , QRect , QUrl , QSize ,QObject
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen ,QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
import cv2,time,sys #,sysinfo
import numpy as np
import random as rnd
from pyqt5cv2 import Tack_Object
#import resources_rc
from pyqt5videoplayer import VideoPlayer
import folium , io , os
from maps import MapCreator
import threading
from qt_thread_updater import get_updater
from threading import Timer 
from collections import defaultdict
import folium
import math,sys,threading,selectors,time,pickle,traceback
import socket, pickle,os,socket,sys,selectors,traceback,threading,sys,time,math,cv2
#sys.path.insert(1, r'C:\Users\MERT ÜNÜBOL\Desktop\SİHA-Workplace\src\modules')
import telemetry_data
import libclient
######TX Variables#########
incoming_roll = 1500
incoming_yaw = 1500
incoming_pitch = 1500
incoming_altitude = 0
incoming_latitude = 0
incoming_long = 32.78342
incoming_enemy_id = 0
incoming_distance = 0
incoming_request = 0
incoming_longitude = 0
incoming_wait_ready_request = 0
tx_data = defaultdict(list)
point_to_track = {"enemy_id":0,"predicted_lat":0,"predicted_lon":0}
plane_to_track = 0
in_range_list = [-1,-1,-1]
#GUI Parameters
otonom_kalkış_cmd = False  
otonom_iniş_cmd = False  
Manual_cmd = False  
kamikaze_cmd = False  
otonom_it_dalaşı_cmd = False 
loiter_cmd = False 
guided_cmd = False
rtl_cmd= False
sel = 0
start = 0
start2 = 0
in_waiting = False
our_telemetry = 0
window_initialized = False
prev_drawing = []
drawing_initialized = False
waiting_data_to_draw = False
mode_1  = "Otonom"
mode_2 = "Manuel"
mode = "Otonom"
locking_count = 0
transmit_stopped = False
transmit_start = False
mission_start = False
client_socket_uav = 0
message_ready = False
#Localizasyon Parameters
Latitude_pts = []
Longitude_pts = []
Altitude_pts = []
enemy_list  = 0
team_number = 1
prev_distance_list = {}
counter = 0
prev_coordinates = []
enemy_prev_list = []
previous_location_list = []
coordinates_prev = (0,0)
z = 0
k = 0
p = 0
count = 0
host = "127.0.0.1"
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname) 
uav_host = IPAddr
uav_port = 65433
port = 65432
start2 = 0
enemy_list_prev = 0
recording = False
record_stopped = True
videoRecorder = 0
class ServerConnection:
    def create_post_value(value):
        request_post = {
        "/api/telemetri_gonder":telemetry_data.telemetry_data,
        "/api/kilitlenme_bilgisi":telemetry_data.lock_on_data,
        "/api/giris":telemetry_data.login,
        "/api/kamikaze_bilgisi":telemetry_data.kamikaze_list,
        }
        sent = request_post[value]
        return  sent
    def create_request(action, value):
        if action == 'post':
            sent = ServerConnection.create_post_value(value=value)
        else:
            sent = "Nothing sent"
        if action == "get" or action == "post":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value ,sent = sent ),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action + value + sent, encoding="utf-8"),
            )

    

    def start_connection(host, port,action, request):
        global sel
        addr = (host, port)
        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(addr)
        sock.setblocking(False)
        sock.connect_ex(addr)
        sel = selectors.DefaultSelector()
        events =  selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libclient.Message(sel, sock, addr, request)
        sel.register(sock, events, data=message)


def Communication():
                global start
                global host
                global port
                global enemy_list
                global enemy_list_prev
                global prev_drawing
                global drawing_initialized
                global client_socket_uav
                global tx_data
                global message_ready
                action = "get"
                value = "/api/telemetri_gonder"
                request = ServerConnection.create_request(action, value)
                ServerConnection.start_connection(host, port,action,request)
                try:
                    while True:
                        events = sel.select(timeout=0)
                        for key, mask in events:
                            message = key.data
                            try:
                                enemy_list = message.process_events(mask)
                                
                                if enemy_list == enemy_list_prev :
                                    enemy_list = 0
                                
                                """ if enemy_list != 0 :
                                    enemy_list_copy = enemy_list
                                    #enemy_list_copy = pickle.dumps(enemy_list_copy)
                                    tx_data = pickle.dumps(tx_data)
                                    enemy_list_prev = enemy_list
                                    if tx_data != 0 :
                                        client_socket_uav.send(tx_data)  # send message """
        
                                if drawing_initialized == False and enemy_list != 0:
                                    if enemy_list == [0,0]:
                                        drawing_initialized = False
                                    else:
                                        dummy_count = 0
                                        for i in range(len(enemy_list)):
                                            prev_drawing.append([])
                                            for j in range(len(enemy_list[0])):
                                                prev_drawing[i].append([0,0,0])
                                                dummy_count += 1
                                        drawing_initialized = True
                            except Exception:
                                print(
                                    f"Main: Error: Exception for {message.addr}:\n"
                                    f"{traceback.format_exc()}"
                                )
                                message.close()
                                #self.client_socket_uav.close()  # close the connection
                        # Check for a socket being monitored to continue.
                        if not sel.get_map():
                            break
                except KeyboardInterrupt:
                    print("Caught keyboard interrupt, exiting")
                finally:
                    #self.client_socket_uav.close()  # close the connection
                    sel.close()

class RepeatTimer(Timer):  
    def run(self):  
        global transmit_stopped
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  
            print(' ')  
            if transmit_stopped == True:
                break

class ThreadClass(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)
    FPS = pyqtSignal(int)
    global camIndex 
    global recording
    global record_stopped
    global videoRecorder
    def run(self):
        self.recording = recording
        self.record_stopped = record_stopped
        if camIndex == 0:
            Capture = cv2.VideoCapture(camIndex)
        if camIndex == 1:
            Capture = cv2.VideoCapture(camIndex,cv2.CAP_DSHOW)

        Capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        Capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        self.ThreadActive = True
        prev_frame_time = 0
        new_frame_time = 0
        while self.ThreadActive:
            ret,frame_cap = Capture.read()
            if self.recording and videoRecorder != 0:
                videoRecorder.write(self.frame)
            if self.record_stopped and videoRecorder != 0:
                videoRecorder.release()
            """ flip_frame = cv2.flip(src=frame_cap,flipCode=-1) """
            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            if ret:
                self.ImageUpdate.emit(frame_cap)
                self.FPS.emit(fps)

    def stop(self):
        self.ThreadActive = False
        self.quit()

class SecondWindows(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.second_window = uic.loadUi(r"C:\Users\MERT ÜNÜBOL\CYCLOP\GLADOS\operators\Security_Camera\secondwindow.ui",self)
        self.videoplayer = " "
    def load_action(self,action):
        if action != "VideoRecordings":
            if self.videoplayer != " ":
                self.videoplayer.deleteLater()
                self.videoplayer = " "
        if action == "LatLon":
            self.setWindowTitle("Enlem Boylam Kayıtları")
        
            pass
        elif action == "Altitude":
            self.setWindowTitle("İrtifa Kayıtları")
            pass
        elif action == "PitchYawRoll":
            self.setWindowTitle("Gyrometer Kayıtları")
            pass
        elif action == "PWM":
            self.setWindowTitle("PWM Kayıtları")
            pass
        elif action == "VideoRecordings":
            self.setWindowTitle("Video Kayıtları")
            self.videoplayer = VideoPlayer(aPath=r"C:\Users\MERT ÜNÜBOL\CYCLOP\GLADOS\operators\website\data")
            self.videoplayer.setAcceptDrops(True)
            self.videoplayer.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            #self.videoplayer.setGeometry(100, 300, 600, 380)
            self.videoplayer.setContextMenuPolicy(Qt.CustomContextMenu)
            self.setCentralWidget(self.videoplayer) 
            
            self.videoplayer.show()
            pass
        elif action == "ContestVideoRecordings":
            self.setWindowTitle("Yarışma Video Kayıtları")
            pass

class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.diff2 = 0
        self.start2 = 0
        self.app = app
        self.ui = uic.loadUi(r"C:\Users\MERT ÜNÜBOL\CYCLOP\GLADOS\operators\Security_Camera\vecihigui.ui",self)
        self.second_windowui = SecondWindows(app)
        self.MAPOBJECT =MapCreator()
        self.recording = False
        self.record_stopped = False
        self._fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self._out = cv2.VideoWriter("output.mp4", self._fourcc, 20.0, (640,480))
        videoRecorder = self._out
        self.online_cam = QCameraInfo.availableCameras()
        self.setGeometry(340,140,1240,860)
        self.pushButton_2.clicked.connect(self.StartWebCam)
        self.pushButton_3.clicked.connect(self.StopWebcam)
        self.actionEnlem_Boylam_Kay_tlar.triggered.connect(lambda: self.showSecondWindow("LatLon"))
        self.action_rtifa_Kay_tlar.triggered.connect(lambda: self.showSecondWindow("Altitude"))
        self.actionPitch_Yaw_Roll_Kay_tlar.triggered.connect(lambda: self.showSecondWindow("PitchYawRoll"))
        self.actionPWM_Kay_tlar.triggered.connect(lambda: self.showSecondWindow("PWM"))
        self.actionVideo_Kay_tlar.triggered.connect(lambda: self.showSecondWindow("VideoRecordings"))
        self.actionYar_ma_Video_Kay_tlar.triggered.connect(lambda: self.showSecondWindow("ContestVideoRecordings"))
        self.pushButton_13.clicked.connect(self.Transmit_Basla)
        self.pushButton_14.clicked.connect(self.ServerOut)
        self.setStyleSheet("""
        QMenuBar {
            background-color: rgb(49,49,49);
            color: rgb(255,255,255);
            border: 1px solid #000;
        }

        QMenuBar::item {
            background-color: rgb(49,49,49);
            color: rgb(255,255,255);
        }

        QMenuBar::item::selected {
            background-color: rgb(30,30,30);
        }

        QMenu {
            background-color: rgb(49,49,49);
            color: rgb(255,255,255);
            border: 1px solid #000;
        }

        QMenu::item::selected {
            background-color: rgb(30,30,30);
        }

        QMainWindow {
            background-color: #554f38;
        }

        """)
        self.lcd_timer = QTimer()
        self.lcd_timer.timeout.connect(self.clock)
        self.lcd_timer.start()
        self.Track_Function1 = Tack_Object()
        self.roi_x = 20
        self.roi_y = 20
        self.roi_w = 2000
        self.roi_h = 2000
        self.coordinate = (39.856398, 32.780181)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(10, 399, 571, 491))
        self.verticalLayout_14 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.webEngineView = QWebEngineView(self.scrollAreaWidgetContents)
        self.webEngineView.setObjectName(u"webEngineView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy2)
        self.webEngineView.setMinimumSize(QSize(0, 0))
        self.webEngineView.setUrl(QUrl(u"about:blank"))
        self.verticalLayout_14.addWidget(self.webEngineView)
        self.MAPOBJECT.Create_Map(self.coordinate)
        file_path = os.path.join(os.getcwd(), "output.html")
        local_url = QUrl.fromLocalFile(file_path)
        self.__view = QWebEngineView(self)
        self.__view.setGeometry(QRect(10,395,591,461))
        self.__view.setUrl(QUrl(local_url))
        self.map_layout = QVBoxLayout()
        self.map_layout.setGeometry(QRect(10,395,591,461))
        self.map_layout.addWidget(self.__view)
        self.show()
        self.enable_update = False

    def update_map(self):
        global drawing_initialized
        global enemy_list
        global prev_drawing
        global our_telemetry
        if self.enable_update:
            our_telemetry = self.MAPOBJECT.UpdateMap(drawing_initialized,enemy_list)
            self.__view.reload()

    def showSecondWindow(self,action):
        self.second_windowui.load_action(action=action)
        self.second_windowui.show()

    def clock(self):
        from datetime import datetime
        global our_telemetry
        self.DateTime = QDateTime.currentDateTime()
        self.DateTime = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        self.lcdNumber.display(self.DateTime)

        if self.start2 == 0:
            self.start2 = datetime.now()
        self.diff2 = (datetime.now() - self.start2).seconds 
        if self.diff2 == 1:
            
            if our_telemetry != 0:
                self.label_telemetry.setWordWrap(True)
                self.label_telemetry.setScaledContents(True)
                self.label_telemetry.setText(str(our_telemetry))
            self.enable_update = True
            self.update_map()
            self.start2 = 0
    def set_roi(self):
        if self.btn_roi_set.isChecked():
            self.btn_roi_set.setText('RESET')
            self.ckb_roi.setChecked(False)
            self.ROI_X.setEnabled(False)
            self.ROI_Y.setEnabled(False)
            self.ROI_W.setEnabled(False)
            self.ROI_H.setEnabled(False)
        else:
            self.btn_roi_set.setText('SET')
            self.ckb_roi.setChecked(True)
            self.ROI_X.setEnabled(True)
            self.ROI_Y.setEnabled(True)
            self.ROI_W.setEnabled(True)
            self.ROI_H.setEnabled(True)

    def Sunucu_Bağlan(self):
        global transmit_start 
        transmit_start = True
        
    def ServerOut(self):
        global transmit_stopped
        transmit_stopped = True 
    def Transmit_Basla(self):
        """ global transmit_start
        if transmit_start == True :
            timer = RepeatTimer(1,Communication)  
            timer.start() #recalling run   """
        timer = RepeatTimer(1,Communication)  
        timer.start() #recalling run
        
    @pyqtSlot(np.ndarray)
    def opencv_emit(self, Image):

        #QPixmap format
        original = self.cvt_cv_qt(Image)
        #Numpy Array format
        self.CopyImage =  Image[self.roi_y:self.roi_h,
                                self.roi_x:self.roi_w]


        self.label_camera.setPixmap(original)
        self.label_camera.setScaledContents(True)


        # Display Object Tracking
        if self.pushButton_2.isChecked():

            Track_object1 = self.Track_Function1.track_object(Image=self.CopyImage,
                                                                  HSVLower=self.hsvOne_lower,
                                                                  HSVUpper=self.hsvOne_upper,
                                                                  Color=self.RanColor1)
        # Get value object
            self.value_curr_object1 = self.Track_Function1.get_current()
            self.value_total_object1 = self.Track_Function1.get_total()

        # Get object in screen
            #self.IsObject1 = self.Track_Function1.check_object()

        # Show object value to lcdNumber
            """ self.lcd_curr_object1.display(self.value_curr_object1)
            self.lcd_object1.display(self.value_total_object1) """

        # Convert function from Numpy to QPixmap
            cvt2Tack_1 = self.cvt_cv_qt(Track_object1)

        # Show on the main screen
            self.label_camera.setPixmap(cvt2Tack_1)
            self.label_camera.setScaledContents(True)



    def get_ROIX(self,x):
        self.roi_x = x

    def get_ROIY(self,y):
        self.roi_y = y

    def get_ROIW(self,w):
        self.roi_w = w

    def get_ROIH(self,h):
        self.roi_h = h

    def cvt_cv_qt(self, Image):
        offset = 5
        rgb_img = cv2.cvtColor(src=Image,code=cv2.COLOR_BGR2RGB)
        if self.pushButton_2.isChecked():
            rgb_img = cv2.rectangle(rgb_img,
                                         pt1=(self.roi_x,self.roi_y),
                                         pt2=(self.roi_w,self.roi_h),
                                         color=(0,255,255),
                                         thickness=2)

        h,w,ch = rgb_img.shape
        bytes_per_line = ch * w
        cvt2QtFormat = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(cvt2QtFormat)
        if self.pushButton_2.isChecked():

            pixmap = QPixmap.fromImage(cvt2QtFormat)
            painter = QPainter(pixmap)
            pen = QPen(Qt.red,3)
            painter.setPen(pen)
            painter.drawRect(self.roi_x-(self.roi_x-offset),
                             self.roi_y-(self.roi_y-offset),
                             self.roi_w-30,
                             self.roi_h-30
                             )

        return pixmap #QPixmap.fromImage(cvt2QtFormat)



    def StartWebCam(self,pin):
        global record_stopped
        global recording
        recording = True
        record_stopped = False
        try:
            global camIndex
            camIndex = 0

        # Opencv QThread
            self.Worker1_Opencv = ThreadClass()
            self.Worker1_Opencv.ImageUpdate.connect(self.opencv_emit)
            self.Worker1_Opencv.start()


        except Exception as error :
            pass

    def StopWebcam(self,pin):
        global record_stopped
        global recording
        recording = False
        record_stopped = True
        self.Worker1_Opencv.stop()

    def Close_software(self):
        self.Worker1_Opencv.stop()
        self.resource_usage.stop()
        sys.exit(self.app.exec_())

app = QApplication([])
window = MainWindow(app)
sys.exit(app.exec_())