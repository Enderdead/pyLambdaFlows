import numpy as np
import time
import pyLambdaFlows
import click
import pandas as pd

t1 = time.time()
N = 10

loopcounts = [(2,N),]*N 

source = pyLambdaFlows.Source()
compute_op = pyLambdaFlows.Map(source, "./compute.py")


sess = pyLambdaFlows.Session(credentials_csv="./accessKeys.csv")
compute_op.compile(sess=sess, purge=False)
promess = compute_op.eval(feed_dict={source: loopcounts}, wait=False, sess=sess)

for i in range(15):
    time.sleep(0.2)
    print(promess.getStatus())