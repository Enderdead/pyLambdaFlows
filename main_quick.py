"""
Quick main for call lambda only.
Only call lambda created on AWS server
"""
import boto3
import json
from S3manager import *
from createRequest import createRequest
from threading import Thread
import progressbar
BUCKET_NAME = "mean-stuff-123"

S3Client = boto3.client('s3',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")


# Clear bucket
print("Clear bucket ...")
clearBucket(BUCKET_NAME)




#Create list of request to do 
requestList = createRequest(BUCKET_NAME)


# Call lambda asyncronly
lambda_client = boto3.client('lambda',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")

print("Send Json request and init computation !")
for request in progressbar.progressbar(requestList):

    def lol():
        lambda_client.invoke(
        FunctionName='LocalMean',
        InvocationType='Event',
        Payload=json.dumps(request),)
    Thread(target=lol).start()
   


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