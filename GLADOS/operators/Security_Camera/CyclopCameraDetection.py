import cv2
from Security_Camera.CyclopNotificationSender import *
import logging , os
import time
import datetime
import pygame
from  Security_Camera.CyclopNotifications import Notification
from Security_Camera.CyclopVideoWriter import VideoWriter
logging.basicConfig(filename='app.log',level=logging.DEBUG)
pygame.mixer.init()


class VideoCamera(object):
    binary = True
    def __init__(self, config , camera_count):
        self.config = config
        self.cam_list = []
        for i in range(camera_count):
            self.cam_list.append(cv2.VideoCapture(i))
        #self.video = cv2.VideoCapture(int(self.config.get('Video')['camera']))
        self.videoWriter = None
        self.online = False
        self.recording = False
        self.first_captured = None
        self.notification = Notification(config) if config.is_exist('Notifications', 'pushover') else None
        self.channel = "0"
        self.do_run = True
        self.frame_list = []
        
    def __del__(self,cam_number):
        self.cam_list[cam_number].release()
        
    def finished(self):
        for i in range(len(self.cam_list)):
            self.cam_list[i].release()
        #self.video.release()
        #self.notification.release()

    def start(self,sens, method, mail, sound, notif , cam_number):
        logging.info('Active security started at ' + str(datetime.datetime.now()))
        iterator = 0
        repeated = 0
        sequence_capture = False
        self.first_captured = None
        self.cam_list[cam_number] = cv2.VideoCapture(cam_number)
        while getattr(self , "do_run" , True):
            success , image = self.cam_list[cam_number].read()
            #success, image = self.video.read()
            if not success:
                continue
            iterator += 1
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if method == 'face':
                faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            #elif method == 'ubody':
                #faceCascade = cv2.CascadeClassifier("haarcascade/haarcascade_upperbody.xml")
            elif method == 'fbody':
                faceCascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
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
                # todo export arguments to config file
                faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=4)
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
                break
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
                continue
            if iterator == 10:
                iterator = 0
                repeated = 0
        self.__del__(cam_number)

    def record(self,upload, cloud ,cam_number):
        self.videoWritertopath = VideoWriter("0")
        self.recording = True
        logging.info('Video recording started at ' + str(datetime.datetime.now()))
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.cam_list[cam_number] = cv2.VideoCapture(0)
        
        #videoWriter = cv2.VideoWriter(self.config.get('File')['videos']+ 'video' + timestr + ".mp4",fourcc, int(self.config.get('Video')['fps']),(640,480))
        while self.recording:
            while True:
                success, image = self.cam_list[cam_number].read()
                cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
                if not success:
                    break
                else:
                    print("......")
                    #videoWriter.write(image)
                    self.videoWritertopath.add_frame(image)
                if self.recording == False :
                    print("Recording stopped")
                    #videoWriter.release() 
                    self.finished()
                    break
                cv2.imshow('frame',image)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
                    #break
        self.videoWritertopath.write()
        #videoWriter.release()
        from Security_Camera.CyclopVideoManager import VideoManager
        manager = VideoManager()
        file_names , full_static_file_names = manager.get_static_video_filenames("webm")
        """ if upload:
            for index,file in enumerate(file_names):
                cloud.upload_file(full_static_file_names[index], file) """

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