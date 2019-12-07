import pyLambdaFlows
from random import randint

a = pyLambdaFlows.op.Source()

b = pyLambdaFlows.op.Source()

c = pyLambdaFlows.op.Map([a,b], "./source/addition.py")

d = pyLambdaFlows.op.Reduce(c, "./source/mean.py")

e = pyLambdaFlows.op.Reduce(c, "./source/mean2.py", name="troololo")


f = pyLambdaFlows.op.Reduce([d,e], "./source/addition.py")

json = None

with pyLambdaFlows.Session(credentials_csv="./accessKeys.csv") as sess:
    f.compile(purge=True)
    result = f.eval(feed_dict={a:[1,2,1], b:[1,2,3]})
    print(result)
    