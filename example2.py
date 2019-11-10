import pyLambdaFlows


with pyLambdaFlows.Session(aws_access_key_id="AKIA2IEN5IAPGJRZQAMQ", aws_secret_access_key="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") as sess:
    a = pyLambdaFlows.upload.Uploader(sess)
    a.upload_lambda("./test.py")

