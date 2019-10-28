import json
from decimal import Decimal
import boto3
import pickle
def lambda_handler(event, context):
    # Get all event data
    idx   = event["idx"]
    eleve = event["data"]
    bucketName = event["bucket"]
    nextEventName, nextEventContent = event.get("nextEvent",(None, None))

    # Compute data
    moyenneGeneral = int(eleve["math"]) + int(eleve["francais"]) + int(eleve["histoire"]) +\
        + int(eleve["tecno"]) + int(eleve["sport"])
    moyenneGeneral /= 5


    # Save data 
    S3Client = boto3.client('s3')
    S3Client.put_object(Body = pickle.dumps(moyenneGeneral), Bucket=bucketName, Key=idx)

    # Call nextOne
    if (not nextEventName is None) and (not nextEventContent is None):
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