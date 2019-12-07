import pyLambdaFlows
from random import randint

a = pyLambdaFlows.op.Source()

b = pyLambdaFlows.op.Source()

c = pyLambdaFlows.op.Map([a,b], "./source/addition.py")

d = pyLambdaFlows.op.Reduce(c, "./source/mean.py")
json = None

with pyLambdaFlows.Session(credentials_csv="./accessKeys.csv", auto_purge=True) as sess:
    d.compile(purge=False)
    result = d.eval(feed_dict={a:[1,2,1], b:[1,2,3]})
    print(result)
    