import pyLambdaFlows
from random import randint

def double(x):
    return x*x

def mean(liste):
    return mean(liste)

a = pyLambdaFlows.op.Source()

b = pyLambdaFlows.op.Map(a, "./source/compute.py")

c = pyLambdaFlows.op.Reduce(b, "./source/mean.py")
json = None

with pyLambdaFlows.Session(aws_access_key_id="AKIA2IEN5IAPGJRZQAMQ", aws_secret_access_key="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") as sess:
    c.compile(purge=False)
    result = c.eval(feed_dict={a:[1,2,3]})
    print(result)
    data = list()
    for i in range(1000):
        data.append(randint(0,100))
    result = c.eval(feed_dict={a:data})
    print(result)
    

