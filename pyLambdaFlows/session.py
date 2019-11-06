from boto3 import client
from botocore.exceptions import ClientError

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
    def __init__(self, region_name="eu-west-3", aws_access_key_id=None, aws_secret_access_key=None):
        self.region = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_access_key_id
        self.clients = dict(IAM=None, Lambda=None, DynamoDb=None)

    def __enter__(self):
        set_default_session(self)

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
