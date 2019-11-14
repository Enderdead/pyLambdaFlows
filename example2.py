import pyLambdaFlows

sess = pyLambdaFlows.Session(credentials_csv="./accessKeys.csv")

a = pyLambdaFlows.upload.Uploader(sess)
a.upload_lambda("./source/mean.py")


