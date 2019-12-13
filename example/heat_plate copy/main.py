import pyLambdaFlows
from conv_op import ConvOp
NB_IT = 6
SIZE = 50
MAX = 1.
# 100 - 3
DATA = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

for i in range(SIZE):
    DATA[i][0] = MAX
    DATA[i][-1] = MAX
    DATA[0][i] = MAX 
    DATA[-1][i] = MAX


source = pyLambdaFlows.Source()

operation = ConvOp(source, "./lambda_kernel.py",name="iteration_0")

for i in range(NB_IT-1):
    operation = ConvOp(operation, "./lambda_kernel.py", name="iteration_{}".format(i))

sess =  pyLambdaFlows.Session(credentials_csv="./accessKeys.csv")
operation.compile(sess=sess)
res = operation.eval(feed_dict={source:DATA}, sess=sess)

