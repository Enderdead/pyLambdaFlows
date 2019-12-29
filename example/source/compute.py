from pyLambdaFlows.decorator import kernel

@kernel 
def lambda_handler(inputData):
    return inputData*inputData
