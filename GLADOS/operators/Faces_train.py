import cv2
import os
import numpy as np
from PIL import Image
import pickle

class Glados_MachineLearn():
	def __init__(self):
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		self.image_dir = os.path.join(self.BASE_DIR, "images")	
		self.trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		self.recognizer = cv2.face.LBPHFaceRecognizer_create()

	def face_train(self):	
		print(self.image_dir)
		current_id = 0
		label_ids = {}
		y_labels = []
		x_train = []

		for root, dirs, files in os.walk(self.image_dir):
			for file in files:
				if file.endswith("png") or file.endswith("jpeg"):
					path = os.path.join(root, file)
					name = os.path.basename(root).lower()
					label = os.path.basename(root).replace(" ", "-").lower()
					#print(label, path)
					if not label in label_ids:
						label_ids[label] = current_id
						current_id += 1
					id_ = label_ids[label]
					#print(label_ids)
					#y_labels.append(label) # some number
					#x_train.append(path) # verify this image, turn into a NUMPY arrray, GRAY
					pil_image = Image.open(path).convert("L") # grayscale
					size = (550, 550)
					final_image = pil_image.resize(size, Image.ANTIALIAS)
					image_array = np.array(final_image, "uint8")
					#print(image_array)
					faces = self.trained_face_data.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

					for (x,y,w,h) in faces:
						roi = image_array[y:y+h, x:x+w]
						x_train.append(roi)
						y_labels.append(id_)


		print(y_labels)
		print(x_train)
		
		with open("labels.pickle", 'wb') as f:
			pickle.dump(label_ids, f)
			print(label_ids)
		self.recognizer.train(x_train, np.array(y_labels))
		self.recognizer.save("face-trainner.yml")

		return name