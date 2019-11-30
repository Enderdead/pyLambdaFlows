import json
import pickle
from time import sleep
import boto3 
from pyLambdaFlows.decorator import kernel


@kernel 
def lambda_handler(inputData):
    
    #inputData = [ element[0] for element in inputData]
    return inputData[0]*inputData[0]
