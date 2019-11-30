import json
import pickle
from time import sleep
import boto3 
from statistics import mean

from pyLambdaFlows.decorator import kernel


@kernel
def lambda_handler(inputData):

    inputData = [element[0] for element in inputData]
    result = mean(inputData)
    inputData = [result,]

    return inputData