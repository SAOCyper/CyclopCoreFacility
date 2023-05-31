import numpy as np
import cv2
import pickle
import serial
import time
import os
import pathlib

class GladosCamera:

    def __init__(self,cap,recognizer,trained_face_data,labels,arduino):
        self.path=pathlib.Path(__file__).parent.resolve()
        os.chdir(self.path)
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        self.counter =0
        self.cap=cap
        self.recognizer=recognizer
        self.trained_face_data=trained_face_data
        self.labels=labels
        self.arduino=arduino
        #self.arduino = serial.Serial(port="com3", baudrate=9600, timeout=.1)
        
    def Camera(self):
        
        
        while True:
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
                        yatay=int((x+x+w)/2)
                        dikey=int((y+y+h)/2)
                        if conf>=4 or conf <= 85:
                            #print(5: #id_)
                            #print(labels[id_])
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            name = self.labels[id_]
                            color = (255, 255, 255)
                            stroke = 2
                            
                            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                        
                        color = (255, 0, 0) #BGR 0-255 
                        stroke = 2
                        end_cord_x = x + w
                        end_cord_y = y + h
                        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
                        if 0<yatay<horizontalboundary1:
                            print("Left")
                            num = "l"
                            self.arduino.write(bytes(num, 'utf-8'))
                            time.sleep(0.1)
                            data = self.arduino.readline() 
                            string= data.decode()
                            stripped = string.strip()
                            print(stripped)
                            break    
                        elif horizontalboundary2<yatay<640 :  
                            print("Right") 
                            num = "r"
                            self.arduino.write(bytes(num, 'utf-8'))
                            time.sleep(0.1)
                            data = self.arduino.readline()
                            string= data.decode()
                            stripped = string.strip()
                            print(stripped) 
                            break    
                        elif horizontalboundary1<yatay or yatay<horizontalboundary2:
                            print("Stopped")
                            num = "Z"
                            self.arduino.write(bytes(num, 'utf-8'))
                            time.sleep(0.1)
                            data = self.arduino.readline()  
                            """ if 0<dikey<verticalboundary3:
                                print("Upx2")
                                num = "U"
                                self.arduino.write(bytes(num, 'utf-8'))
                                time.sleep(0.01)
                                data = self.arduino.readline()  
                                string= data.decode()
                                stripped = string.strip()
                                print(stripped)
                            elif verticalboundary3<dikey<verticalboundary1:
                                print("Upx1")
                                num = "u"
                                self.arduino.write(bytes(num, 'utf-8'))
                                time.sleep(0.01)
                                data = self.arduino.readline()  
                                string= data.decode()
                                stripped = string.strip()
                                print(stripped)
                            elif verticalboundary1<dikey<verticalboundary2:
                                print("Vertical stopped")
                                num = "z"
                                self.arduino.write(bytes(num, 'utf-8'))
                                time.sleep(0.01)
                                data = self.arduino.readline()  
                                
                            elif verticalboundary2< dikey <verticalboundary4 :
                                print("Downx1")
                                num = "d"
                                self.arduino.write(bytes(num, 'utf-8'))
                                time.sleep(0.01)
                                data = self.arduino.readline()
                                string= data.decode()
                                stripped = string.strip()
                                print(stripped)
                            elif verticalboundary4< dikey <480 :
                                print("Downx2")
                                num = "D"
                                self.arduino.write(bytes(num, 'utf-8'))
                                time.sleep(0.01)
                                data = self.arduino.readline()
                                string= data.decode()
                                stripped = string.strip()
                                print(stripped) """
                            break         
                else:
                    print("Find1")
                    num = "F"
                    self.arduino.write(bytes(num, 'utf-8'))
                    time.sleep(0.1)
                    data = self.arduino.readline()
                    string= data.decode()
                    stripped = string.strip()
                    print(stripped)
                    
                # Display the resulting frame
                cv2.imshow('frame',frame)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    print("....RESETTING CAMERA....")
                    num = "S"
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

