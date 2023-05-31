from imutils.video import FPS
import numpy as np
import cv2
import face_recognition

class GladosCamera:
    trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    webcam = cv2.VideoCapture(0)
    fps = FPS().start()
    mert_image = face_recognition.load_image_file("Mertunubol.jpeg")
    volkan_image = face_recognition.load_image_file("VolkanDemirel.jpeg")
    mert_face_encoding = face_recognition.face_encodings(mert_image, model= "MODEL")[0]
    volkan_face_encoding = face_recognition.face_encodings(volkan_image, model= "MODEL")[0]

    known_face_encodings = [
        mert_face_encoding,
        volkan_face_encoding
    ]
    known_face_names = [
        "Mert unubol",
        "Volkan Demirel"
    ]
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        process_this_frame = True
        fps.update()
        successful_frame_read , frame = webcam.read()
        face_coordinates = trained_face_data.detectMultiScale(frame)
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(frame, 1)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
                
            process_this_frame = not process_this_frame
        for (x, y, h, w) in face_coordinates :
            cv2.rectangle(frame, (x,y),(x+h,y+w),(0,0,255),3)
            cv2.rectangle(frame, (x, y+w - 35), (x+h, y+w), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame,name, (x + 10, y+w - 6), font, 0.75, (255, 255, 255), 1)
            cv2.imshow("Output",frame)
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    webcam.release()
    cv2.destroyAllWindows()






