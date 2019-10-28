"""
Create lamnbda function with AWS API.
- Create zip file
- Send the raw file with API 
"""
import zipfile, os
import boto3
import progressbar
# Connect to AWS API

iam_client = boto3.client('iam',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")


lambda_client = boto3.client('lambda',
    aws_access_key_id='AKIA2IEN5IAPGJRZQAMQ',
    aws_secret_access_key='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',
    region_name="eu-west-3")
env_variables = dict() 
role = iam_client.get_role(RoleName='LambdaBasicExecution')


FILES = ["calculMoyen.py", "calculClasse.py", "calculMoyenEtabl.py" ]
ZIPNAME = ["mean.zip", "classes.zip", "etabli.zip"]
LAMBDA_NAME = ["LocalMean", "ClassMean", "MeanEta"]
FUNC_NAME = ["calculMoyen.lambda_handler", "calculClasse.lambda_handler", "calculMoyenEtabl.lambda_handler" ]

print(" Lambda creation !")
if not os.path.exists(os.path.join(os.path.curdir, "bin")):
    os.makedirs(os.path.join(os.path.curdir, "bin"))

for fil, zipe, lambda_, funcName in progressbar.progressbar( list(zip(FILES, ZIPNAME, LAMBDA_NAME, FUNC_NAME))):

    #TODO improve files serialization with a diskless solution.
    # Create a zip file
    with zipfile.ZipFile (os.path.join(os.path.curdir, "bin",zipe), "w") as zipObj:
        zipObj.write(os.path.join(os.path.curdir,"source",fil), fil )

    # Read bytes file
    with open(os.path.join(os.path.curdir,"bin",zipe), 'rb') as f:
        zipped_code = f.read()


    # Remove if lambda already exist
    try:
        lambda_client.delete_function(FunctionName=lambda_)
    except:
        pass

    lambda_client.create_function(
        FunctionName=lambda_,
        Runtime='python3.7',
        Role=role['Role']['Arn'],
        Handler=funcName,
        Code=dict(ZipFile=zipped_code),
        Timeout=300, # Maximum allowable timeout
        )