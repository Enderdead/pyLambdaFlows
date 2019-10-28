"""
Main file to execute for all project process

Create lambda
Create bucket
Generate json request
Call lamnda AWS
Check S3 bucket for result back up
"""
import boto3
import json
import progressbar
from S3manager import *
from createRequest import createRequest
BUCKET_NAME = "mean-stuff-123"

#Init Boto3
lambda_client = boto3.client('lambda',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")

S3Client = boto3.client('s3',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")


# Create bucket for result gathering
print("Create bucket ...")
create_bucket(BUCKET_NAME)

# Create lambda 
from createLambda import * 

#Create list of request to do 
requestList = createRequest(BUCKET_NAME)


# Call lambda asyncronly



print("Send Json request and init computation !")
for request in progressbar.progressbar(requestList):
    lambda_client.invoke(
        FunctionName='LocalMean',
        InvocationType='Event',
        Payload=json.dumps(request),
    )

print("Computation got started ! ")
for i in progressbar.progressbar(range(31,35)):
    receive= False
    if(i==32):
        continue
    while not receive:
        try:
            S3Client.get_object(Bucket="mean-stuff-123", Key=str(i))
            receive = True
        except Exception:
            pass
print("Memory S3 dump")
from dumpMemory import *