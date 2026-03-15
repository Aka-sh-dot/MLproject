import pickle
import json
import config
import numpy as np

class MedicalInsurance():
    def __init__(self,age,gender,bmi,children,region):
        self.age= age
        self.gender = gender
        self.bmi = bmi
        self.children =children
        self.region = region
        
    def load_model(self):
        with open(config.model_path,"rb") as file:
            self.dt_clf = pickle.load(file)

        # json file
        with open(config.json_path,"r") as file:
            self.label_enc_data = json.load(file)
    def get_charges(self):
        self.load_model()
    
        test_array = np.zeros((1,len(self.label_enc_data["columns_name"])))

        test_array[0,0] = self.label_enc_data["gender"][self.gender] 
        region_1 = "region_" + self.region
        index_region = self.label_enc_data["columns_name"].index(region_1)
        test_array[0,index_region] = 1

        test_array[0,5] = 0 if self.age <=18 else 1 if self.age <=35 else 2 if self.age <= 50 else 3

        test_array[0,6] =  0 if self.bmi <= 18.5 else 1 if self.bmi <= 24.9 else 2 if self.bmi <= 29.9 else 3 

        test_array[0,7] = self.children + 1
        prediction_user_data = self.dt_clf.predict(test_array)
        print("Predicted charges are ",prediction_user_data[0])

        return prediction_user_data[0]