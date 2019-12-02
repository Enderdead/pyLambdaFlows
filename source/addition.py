import json
import pickle
from time import sleep
import boto3 
from pyLambdaFlows.decorator import kernel


@kernel 
def lambda_handler(a, b):
    
    #inputData = [ element[0] for element in inputData]
    return a[0]+b[0]
