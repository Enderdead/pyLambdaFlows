import json
from decimal import Decimal
import boto3
import pickle
from time import sleep
from statistics import mean
def lambda_handler(event, context):
    # Get all event data
    idx   = event["idx"]
    eleves = event["data"]
    bucketName = event["bucket"]
    nextEventName, nextEventContent = event.get("nextEvent",(None, None))

    NoteClass = list()


    # Get all data 
    S3Client = boto3.client('s3')
    for eleve in eleves:
        batchResult = -1
        while batchResult<0:
            try:
                batchResult = float(pickle.loads(S3Client.get_object(Bucket=bucketName, Key=eleve)["Body"].next()))
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

    
    # Call nextOne
    if (not nextEventName is None) and (not nextEventContent  is None):

        lambda_client = boto3.client('lambda')

        lambda_client.invoke(
        FunctionName=nextEventName,
        InvocationType='Event',
        Payload=json.dumps(nextEventContent),
        )
    return {
        'statusCode': 200,
        'body': json.dumps("Ok")
    }   