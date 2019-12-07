import json
import pickle
from time import sleep
import boto3 
from statistics import mean
import decimal


from pyLambdaFlows.decorator import kernel


@kernel
def lambda_handler(inputData):
    result = mean(inputData)
    return result*-1
