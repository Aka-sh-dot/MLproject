import pickle
import json
import config
import numpy as np

class onlinefrauddetection():
    def __init__(self,step,amount,oldbalanceOrg,newbalanceOrig,oldbalanceDest,newbalanceDest,type):

        self.step= step
        self.amount = amount
        self.oldbalanceOrg = oldbalanceOrg
        self.newbalanceOrig =newbalanceOrig
        self.oldbalanceDest = oldbalanceDest
    
        self.newbalanceDest= newbalanceDest
        self.type=type
        
    def load_model(self):
        with open(config.model_path,"rb") as file:
            self.log_model = pickle.load(file)

        # json file
        with open(config.json_path,"r") as file:
            self.label_enc_data = json.load(file)
    def check(self):
        self.load_model()
    
        test_array = np.zeros((1,len(self.label_enc_data["columns_name"])))

        test_array[0,0] =self.step
        test_array[0,1] = self.amount
        test_array[0,2] = self.oldbalanceOrg
        test_array[0,3] = self.newbalanceOrig
        test_array[0,4] = self.oldbalanceDest
        test_array[0,5] = self.newbalanceDest
        type_1 = "type_" + self.type
        index_type = self.label_enc_data["columns_name"].index(type_1)
        test_array[0,index_type] = 1
        
        prediction_user_data = self.log_model.predict(test_array)
        print("Predicted charges are ",prediction_user_data[0])

        return prediction_user_data[0]
    