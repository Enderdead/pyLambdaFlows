import pyLambdaFlows
from random import randint

a = pyLambdaFlows.op.Source()

b = pyLambdaFlows.op.Map(a, "./source/compute.py")

c = pyLambdaFlows.op.Reduce(b, "./source/mean.py")
json = None

with pyLambdaFlows.Session(credentials_csv="./accessKeys.csv") as sess:
    c.compile(purge=False)
    result = c.eval(feed_dict={a:[1,2,3]})
    print(result)
    