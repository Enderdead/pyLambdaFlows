import zipfile, os
import boto3

# Connect to AWS API

iam_client = boto3.client('iam',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")


lambda_client = boto3.client('lambda',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")
env_variables = dict() 
role = iam_client.get_role(RoleName='LambdaBasicExecution')


LAMBDA_NAME = ["LocalMean", "ClassMean", "MeanEta"]

for lambda_ in LAMBDA_NAME:
    # Remove  lambda if exist
    try:
        lambda_client.delete_function(FunctionName=lambda_)
    except:
        pass
