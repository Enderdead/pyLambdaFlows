import pyLambdaFlows

sess = pyLambdaFlows.Session(aws_access_key_id="AKIA2IEN5IAPGJRZQAMQ", aws_secret_access_key="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")

a = pyLambdaFlows.upload.Uploader(sess)
a.upload_lambda("./test.py")


