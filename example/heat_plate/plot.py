import pickle
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
N_TIME = 10000

dataFrame = pd.read_csv("./data.csv",index_col=0)


max_time = dataFrame.max()["end_call"]+10


xs = np.linspace(0,max_time, num=N_TIME)

FLOP_per_instance =  dataFrame.iloc[0]["FLOPS"]



peaks_Gflops = np.zeros_like(xs)
effective_Gflops = np.zeros_like(xs)


for idx, x in enumerate(xs):
    for row in dataFrame.iterrows():
        if row[1]["start_compute"]<x<row[1]["end_compute"]:
            peaks_Gflops[idx] += 1e-9*row[1]["FLOPS"]/(row[1]["end_compute"]-row[1]["start_compute"])
            
        if row[1]["end_call"]<x:
            effective_Gflops[idx]+=  1e-9*row[1]["FLOPS"]/x

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(xs, peaks_Gflops)
ax.plot(xs, effective_Gflops)
ax.set_xlabel('time (sec)')
ax.set_ylabel("GFLOPS")
plt.show()
