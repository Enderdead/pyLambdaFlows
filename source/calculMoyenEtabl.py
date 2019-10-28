import json
from decimal import Decimal
import boto3
import pickle
from time import sleep
from statistics import mean
def lambda_handler(event, context):
    # Get all event data
    idx   = event["idx"]
    classes = event["data"]
    bucketName = event["bucket"]
    NoteClass = list()


    # Get all data 
    S3Client = boto3.client('s3')
    for classe in classes:
        batchResult = -1
        while batchResult<0:
            try:
                batchResult = float(pickle.loads(S3Client.get_object(Bucket=bucketName, Key=classe)["Body"].next()))
            except:
                pass
            if batchResult>=0:
                NoteClass.append(batchResult)
                break
            sleep(0.2)


    # Compute
   
    result = mean(NoteClass)

    
    # Store data
    S3Client.put_object(Body = pickle.dumps(result), Bucket=bucketName, Key=idx)

    
    return {
        'statusCode': 200,
        'body': json.dumps("Ok")
    }   