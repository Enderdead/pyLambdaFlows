import pyLambdaFlows

def double(x):
    return x*x

def mean(liste):
    return mean(liste)

a = [1,2,3,4]

b = pyLambdaFlows.op.Map(a, double)

c = pyLambdaFlows.op.Reduce(b, mean)
print(c.terminal)

with pyLambdaFlows.Session(aws_access_key_id="1", aws_secret_access_key="1") as sess:
    c.compile()
    c.eval()

