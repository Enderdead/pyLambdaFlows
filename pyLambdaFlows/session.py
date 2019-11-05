from boto3 import client, resource
from botocore.exceptions import ClientError
from pandas import read_csv
_DEFAULT_SESSION = None

def set_default_session(session):
    global _DEFAULT_SESSION
    _DEFAULT_SESSION = session

def get_default_session(check_if_none=False):
    global _DEFAULT_SESSION
    if _DEFAULT_SESSION is None and check_if_none:
        raise RuntimeError("No default session provided, please use kward or set default session !")
    return _DEFAULT_SESSION


class Session():
    def __init__(self, region_name="eu-west-3", aws_access_key_id=None, aws_secret_access_key=None, credentials_csv=None):
        self.region = region_name
        if credentials_csv is None:
            self.aws_access_key_id = aws_access_key_id
            self.aws_secret_access_key = aws_secret_access_key
        else:
            csv_loaded = read_csv(credentials_csv)
            self.aws_access_key_id = csv_loaded.iloc[0]["Access key ID"]
            self.aws_secret_access_key = csv_loaded.iloc[0]["Secret access key"]
        self.clients = dict(IAM=None, Lambda=None, DynamoDb=None, S3=None, Bucket=None)

    def __enter__(self):
        set_default_session(self)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        set_default_session(None)

    def setCredential(self, aws_access_key_id=None, aws_secret_access_key=None):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_access_key_id

    def getIAM(self):
        if( self.aws_access_key_id is None or self.aws_secret_access_key is None):
            raise RuntimeError("Credentials must be provided !")
        if self.clients.get("IAM", None) is None:
            newIamClient = client('iam',
                                    aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key,
                                    region_name=self.region)
            try:
                newIamClient.get_account_summary()
            except ClientError:
                raise RuntimeError("Your credential isn't valid")

            self.clients["IAM"] = newIamClient
        return self.clients["IAM"]

    def getLambda(self):
        if( self.aws_access_key_id is None or self.aws_secret_access_key is None):
            raise RuntimeError("Credentials must be provided !")
        if self.clients.get("Lambda", None) is None:
            newLambdaClient = client('lambda',
                                    aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key,
                                    region_name=self.region)

            try:
                newLambdaClient.list_functions()
            except ClientError:
                raise RuntimeError("Your credential isn't valid")

            self.clients["Lambda"] = newLambdaClient
        return self.clients["Lambda"]

    def getS3(self):
        if( self.aws_access_key_id is None or self.aws_secret_access_key is None):
            raise RuntimeError("Credentials must be provided !")
        if self.clients.get("S3", None) is None:
            newS3Client = client('s3',
                                    aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key,
                                    region_name=self.region)
            self.clients["S3"] = newS3Client
        return self.clients["S3"]

    def getBucket(self):
        if( self.aws_access_key_id is None or self.aws_secret_access_key is None):
            raise RuntimeError("Credentials must be provided !")
        if self.clients.get("Bucket", None) is None:
            newS3Client = resource('s3',
                                    aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key,
                                    region_name=self.region)
            self.clients["Bucket"] = newS3Client
        return self.clients["Bucket"]

    def getDynamoDb(self):
        if( self.aws_access_key_id is None or self.aws_secret_access_key is None):
            raise RuntimeError("Credentials must be provided !")
        if self.clients.get("DynamoDb", None) is None:
            newDynamoClient = client('dynamodb',
                                    aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key,
                                    region_name=self.region)
            try:
                newDynamoClient.list_functions()
            except ClientError:
                raise RuntimeError("Your credential isn't valid")

            self.clients["DynamoDb"] = newDynamoClient
        return self.clients["DynamoDb"]


    def clear(self):
        for key in self.clients.keys():
            self.clients[key] = None

if __name__ == "__main__":
    print(get_default_session())

    with Session() as sess:
        print(get_default_session())

