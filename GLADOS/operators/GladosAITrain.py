import nltk
from nltk.stem import WordNetLemmatizer
from snowballstemmer import stemmer
import random
import numpy as np
import pickle
import json
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout
from keras.optimizers import SGD
""" from keras.optimizer_v1 import SGD """
import os
import pathlib
""" from tensorflow.python.keras.optimizer_v1 import SGD,Adam """
""" from keras.optimizer_experimental import sgd """

class CyclopAITrainer():
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()
    def train(self):
        
        path=pathlib.Path(__file__).parent.resolve()
        os.chdir(path)
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        self.intents = json.loads(open('intents.json').read())
        print(self.intents)
        self.words=[]

        self.classes = []
        self.documents = []
        self.ignore_letters = ['?','!','.',',']
        for intent in self.intents['intents']:
            self.word_list_translated=[]
            for pattern in intent['patterns']:
                self.word_list = nltk.word_tokenize(pattern)
                self.documents.append((self.word_list,intent['tag']))
                self.words.extend(self.word_list)
                if intent['tag']  not in self.classes:
                    self.classes.append(intent['tag']) 
        self.words=[self.lemmatizer.lemmatize(word) for word in self.words if word not in self.ignore_letters]
        self.words = sorted(set(self.words))

        self.classes = sorted(set(self.classes))
        pickle.dump(self.words, open('words.pkl','wb'))
        pickle.dump(self.classes,open('classes.pkl','wb'))

        self.training = []
        self.output_empty = [0] * len(self.classes)
        for document in self.documents:
            bag = []
            word_patterns = document[0]
            word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row = list(self.output_empty)
            output_row[self.classes.index(document[1])] = 1
            self.training.append([bag,output_row])

        random.shuffle(self.training)
        self.training = np.array(self.training)
        self.training_x = list(self.training[:,0])
        self.training_y = list(self.training[:,1])

        self.model = Sequential()
        self.model.add(Dense(128, input_shape=(len(self.training_x[0]),),activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(64,activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(len(self.training_y[0]),activation='softmax'))
        sgdq = SGD(lr=0.01,decay=1e-6,momentum=0.9,nesterov=True)
        self.model.compile(loss='categorical_crossentropy',optimizer=sgdq,metrics=['accuracy'])
        hist=self.model.fit(np.array(self.training_x),np.array(self.training_y),epochs=2500,batch_size=64,verbose=1)
        self.model.save('gladosAI.h5',hist)
        print('Done')

""" tra = CyclopAITrainer()
tra.train() """