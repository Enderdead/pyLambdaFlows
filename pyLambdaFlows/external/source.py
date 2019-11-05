import json
import pickle
from time import sleep
import boto3 

def lambda_handler(event, context):
    ######################################################################################""

    # Get all event data
    idx   = event["idx"]
    source = event["source"]
    data = event["data"]
    children = event["children"]
    bucket = event["bucket"]

    if(source=='direct'):
        inputData = [int(element) for element in data]
    if(source=='data'):
        S3Client = boto3.client('s3')
        for idx_loc in data:
            batchResult = None
            while batchResult is None:
                try:
                    batchResult = pickle.loads(S3Client.get_object(Bucket=bucket, Key=idx_loc)["Body"].next())
                except:
                    sleep(0.2)
                    continue
            inputData.append(batchResult)   
    ######################################################################################""

    # compute 
    # Rien

    ######################################################################################""
    # Store
    S3Client = boto3.client('s3')
    S3Client.put_object(Body = pickle.dumps(inputData), Bucket=bucket, Key=idx)

    # Treatment
    if(len(children.keys()) != 0):
        for _, item in children.items():
            lambda_client = boto3.client('lambda')

            lambda_client.invoke(
            FunctionName=item['func'],
            InvocationType='Event',
            Payload=json.dumps(item),
            )
  
    ######################################################################################""


    return {
        'statusCode': 200,
        'body': json.dumps("Ok")
    }   