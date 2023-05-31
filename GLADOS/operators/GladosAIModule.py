import nltk
from nltk.stem import WordNetLemmatizer
import random
import numpy as np
import pickle
import json
import os
import pathlib
from keras.models import load_model
from mathparse import mathparse
class GladosAIModule:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.path=pathlib.Path(__file__).parent.resolve()
        os.chdir(self.path)
        self.path_parent = os.path.dirname(os.getcwd())
        os.chdir(self.path_parent)
        self.intents = json.loads(open('intents.json').read())
        self.words=pickle.load(open('words.pkl','rb'))
        self.classes=pickle.load(open('classes.pkl','rb'))
        self.model=load_model('gladosAI.h5')

    def clean_up_sentence(self,sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self,sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i,word in enumerate(self.words):
                if word == w:
                    bag[i]= 1
                
        return np.array(bag)

    def predict_class(self,sentence):
        mathematical_response ,mathematical_confidence= self.mathematical_logic_adapters(sentence)
        
        if mathematical_confidence == 0:
            print("not math")
            bow = self.bag_of_words(sentence)
            res = self.model.predict(np.array([bow]))[0]
            ERROR_THRESHOLD = 0.40
            results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
            
            results.sort(key=lambda x: x[1],reverse=True)
            return_list = []
            for r in results:
                return_list.append({'intent':self.classes[r[0]],'probability':str(r[1])})
            return return_list
        if mathematical_confidence == 1:
            return mathematical_response

    def get_response(self,intents_list,intent_json):
        
        if len(intents_list) != 0:
            tag = intents_list[0]['intent']
            probability = intents_list[0]['probability']
            list_of_intents=intent_json['intents']
            for i in list_of_intents:
                if i['tag']== tag:
                    result = random.choice(i['responses'])
                    print("Probability is {}".format(probability))
                    break
        if len(intents_list) == 0:
            result = "Unknown"
        return result
    def mathematical_preprocessors(self,statement):
        list_string = []
        list_string[:0] = statement
        prev_char = "-1"
        comma_detected = False
        unwanted_list = None
        unwanted = ["ün ","nün","nin","in ","un ","nun","ın ","nın","ile","ve ","ye ","yi ","yü ","ya ","dan","den","ten","tan"]
        unwanted2 = ["u","i","ü","ı"]
        conversion_list = ["ekle","çıka","defa","topl","böl"]
        index_number = 0
        for index , char in enumerate(list_string):
            if prev_char.isnumeric() and char == "'" :
                list_string[index_number] = " "
            if char.isnumeric() and comma_detected:
                list_string[index_number - 1] = "."
                comma_detected = False
            if char == "," and prev_char.isnumeric():
                comma_detected = True
            
            unwanted_list = ''.join(list_string[index_number:index_number+3])
            for item in unwanted:
                if item == unwanted_list:
                    list_string = list_string[:index_number] + list_string[index_number+len(unwanted_list):]
                    index_number = index_number- len(unwanted_list)
                
            prev_char = char
            index_number += 1
        prev_char = "-1"
        first_step = False
        convert_condition = False
        convert_flag = False
        last_index = -1
        first_index = -1
        conversion_item = ""
        string_to_add = ""
        cheksum_value = ""
        for index , char in enumerate(list_string):# 5'e 10 eklersem cümlesindeki tekli e,a,u,i,ü yi çıkartıyor
            if first_step and char == " ":
                list_string[index - 1] = " "
                first_step = False
            elif char != " ":
                first_step =False
            if prev_char == " " and (char == 'i' or char == 'e' or char == 'u' or char == 'a' or char =='ü'):
                first_step = True
            
            prev_char = char
        for index , char in enumerate(list_string):
            if convert_condition:
                conversion_item = conversion_item + list_string[index-1]
                if index + 1 == len(list_string) or char == " ":
                    if char == " ":
                        last_index = index - 1
                    if index + 1 == len(list_string):
                        last_index = index
                    convert_condition = False
                    convert_flag = True
            if char == "e" or char == "ç" or char == "d" or char == "t":
                wanted_item = ''.join(list_string[index:index+4])
                for item in conversion_list:
                    if item == wanted_item:
                        cheksum_value = wanted_item
                        first_index = index
                        convert_condition = True
            if convert_flag:
                list_to_add = []
                if cheksum_value == "ekle" or "topl":
                    string_to_add = "artı"
                if cheksum_value == "çıka":
                    string_to_add = "eksi"
                if cheksum_value == "defa":
                    string_to_add = "çarpı"
                list_to_add[:0]=string_to_add
                list_string = list_string[:first_index] + list_to_add + list_string[last_index+1:]
                convert_flag = False
        statement = ''.join(str(x) for x in list_string)
        expression = mathparse.extract_expression(statement, language='TUR')  
        expression = ['*' if 'x'in s else s for s in expression]
        expression = ''.join(str(x) for x in expression)
        return expression
    
    def mathematical_logic_adapters(self,statement):
        expression = self.mathematical_preprocessors(statement)
        try:
            expression = '{} = {}'.format(
                expression,
                mathparse.parse(expression, language='TUR')
            )
            # The confidence is 1 if the expression could be evaluated
            confidence = 1
        except mathparse.PostfixTokenEvaluationException:
            confidence = 0

        return expression , confidence 
""" Aı=GladosAIModule()
while True:
        message = input("")
        ints = Aı.predict_class(message)
        res = Aı.get_response(ints,Aı.intents)
            
        print(res) """