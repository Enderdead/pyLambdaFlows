import numpy as np
import time
from pyLambdaFlows.decorator import kernel
from statistics import mean

@kernel
def lambda_handler(inputData):
    return mean(inputData)