import pyLambdaFlows

def double(x):
    return x*x

def mean(liste):
    return mean(liste)

a = pyLambdaFlows.op.Source()

b = pyLambdaFlows.op.Map(a, double)

c = pyLambdaFlows.op.Reduce(b, mean)
json = None

with pyLambdaFlows.Session(aws_access_key_id="1", aws_secret_access_key="1") as sess:
    c.compile()
    json = c.eval(feed_dict={a:[1,2,3]})
    a = pyLambdaFlows.upload.Uploader(sess)
    

