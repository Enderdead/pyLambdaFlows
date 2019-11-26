import json
import pickle
from time import sleep
import boto3 

@decorate 
def lambda_handler(inputData):
   try:
        for i in range(len(inputData)):
            inputData[i][0] = inputData[i][0]*inputData[i][0]
    except:
        pass
    inputData = [ element[0] for element in inputData]
return inputData