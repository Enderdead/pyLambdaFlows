import numpy as np
import time
import pyLambdaFlows
import click
import pandas as pd
import pickle
t1 = time.time()
N = 100
Workers = 100
loops = 6
loopcounts = [(6,N),]*Workers 

source = pyLambdaFlows.Source()
compute_op = pyLambdaFlows.Map(source, "./compute.py")


sess = pyLambdaFlows.Session(credentials_csv="./accessKeys.csv")
compute_op.compile(sess=sess, purge=False)
start_time = time.time()
promess = compute_op.eval(feed_dict={source: loopcounts}, wait=False, sess=sess)

local_jobs_done_timeline = []
result_count = 0
old = -1
while result_count < Workers:
    _, result_idx = promess.getStatus()
    result_count = len(result_idx)
    print(result_count)
    if old!=result_count:
        local_jobs_done_timeline.append((time.time(), result_idx))
        old = result_count
    
result = promess.getResult()
data_dict = {"start_call" : [], "start_compute": [], "FLOPS": [], "end_compute": [], "end_call": []}

for idx in promess.result_idx:
    start_call = start_time
    start_compute = result[promess.result_idx.index(idx)][1]
    end_compute =  result[promess.result_idx.index(idx)][2]
    flops = result[promess.result_idx.index(idx)][0]
    end_call = start_call
    for timestamp, received in local_jobs_done_timeline:
        if idx in received:
            end_call = timestamp
            break
    data_dict["start_call"].append(start_call-start_time)
    data_dict["start_compute"].append(start_compute-start_time)
    data_dict["end_compute"].append(end_compute-start_time)
    data_dict["FLOPS"].append(flops)
    data_dict["end_call"].append(end_call-start_time)


dataFrame = pd.DataFrame(data_dict)
pickle.dump(dataFrame, open("data.pickle", "wb"))