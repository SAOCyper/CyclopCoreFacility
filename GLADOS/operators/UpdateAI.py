import json
import pathlib
import os
from GladosAITrain import CyclopAITrainer

class UpdateAI():
    def __init__(self):
        path=pathlib.Path(__file__).parent.resolve()
        os.chdir(path)
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        self.trainer = CyclopAITrainer()
    def write_json(self,new_data, filename='intents.json'):
        with open(r'C:\Users\MERT ÜNÜBOL\CYCLOP\GLADOS\intents.json','r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["intents"].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
    
    def  validate_data(self):
        pass
    
    def preprecessor(self,input):
        words_to_throw = ["onceki","soruya","cevabin","bu","olmali","sorunun","cevabi","boyle",""]
        pass

    def learn_new_response(self,inputted , previous_statement):
        with open(r'C:\Users\MERT ÜNÜBOL\CYCLOP\GLADOS\intents_number.txt','r') as file1:
        
            intent_number = file1.readline(1)
            file1.seek(0)
            intent_number = int(intent_number)
            intent_number += 1
            intent_number = str(intent_number)
            file1.close()
        new_data = {"tag":"Learning OverWrites {}".format(intent_number),
                    "patterns":[previous_statement],
                    "responses":[inputted]}
        with open(r'C:\Users\MERT ÜNÜBOL\CYCLOP\GLADOS\intents_number.txt','w') as file1:
        
            file1.write(intent_number)
            file1.close()
            self.write_json(new_data)
        #self.trainer.train()
