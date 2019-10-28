"""
Get all S3 memory link to this project
"""
import logging
import boto3
from botocore.exceptions import ClientError
import pickle

S3Client = boto3.client('s3',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")

for i in range(0,35):
    try:
        res = S3Client.get_object(Bucket="mean-stuff-123", Key=str(i))["Body"]
        print(i, " : ", pickle.loads(res.next()))
    except Exception:
        print(i, " : ", None)


