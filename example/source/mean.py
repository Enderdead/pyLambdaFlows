from pyLambdaFlows.decorator import kernel
from statistics import mean

@kernel
def lambda_handler(inputData):
    result = mean(inputData)
    return result
