"""
Function for S3 API gesture.

"""
import logging
import boto3
from botocore.exceptions import ClientError
import botocore


def _getCredential():
    S3Client = boto3.client('s3',
        aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
        aws_secret_access_key='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',
        region_name="eu-west-3")
    bucketClient = boto3.resource('s3',
        aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
        aws_secret_access_key='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',
        region_name="eu-west-3")
    return S3Client, bucketClient



def create_bucket(name, location="eu-west-3"):
    """
    Create a specific bucket or reset if already exists
    """
    location = {'LocationConstraint': location}
    S3Client, bucketClient = _getCredential()
    try:
        S3Client.create_bucket(Bucket=name, CreateBucketConfiguration=location)
    except botocore.errorfactory.ClientError as e:
        if(e.response["Error"]["Code"]=="BucketAlreadyOwnedByYou"):

            buc = bucketClient.Bucket(name)
            buc.objects.all().delete()
            S3Client.delete_bucket(Bucket=name)

            S3Client.create_bucket(Bucket=name, CreateBucketConfiguration=location)
        else:
            raise e

def clearBucket(name):
    """
    Reset a Specific bucket
    """
    S3Client, bucketClient = _getCredential()
    try:
        buc = bucketClient.Bucket(name)
        buc.objects.all().delete()   
    except botocore.errorfactory.ClientError as e:
        pass

def removeBucket(name):
    """
    Remove a specific bucket
    """
    S3Client, bucketClient = _getCredential()
    try:
        buc = bucketClient.Bucket(name)
        buc.objects.all().delete()
        S3Client.delete_bucket(Bucket=name)
    except botocore.errorfactory.ClientError as e:
        pass