import pyLambdaFlows
from conv_op import ConvOp
import time
import pandas as pd


#

NB_IT = 6
SIZE = 202
MAX = 1.
GATHERING = 2

# 100 - it 3
# 5 - 202 - 10
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

NB_KERNEL = (SIZE-2)/GATHERING
if NB_KERNEL!=int(NB_KERNEL):
    raise RuntimeError("Invalid parameters")

NB_KERNEL+=2
NB_KERNEL = int(NB_KERNEL)
print("Nb Kernel ", NB_KERNEL)
DATA_PER_KERNEL = [list() for i in range(NB_KERNEL)]

DATA_PER_KERNEL[0].append(DATA[0])
DATA_PER_KERNEL[-1].append(DATA[-1])
for i in range(1,SIZE-1):
    DATA_PER_KERNEL[ (i-1)//GATHERING +1].append(DATA[i])


start_time = time.time()
sess =  pyLambdaFlows.Session(credentials_csv="./accessKeys.csv")
operation.compile(sess=sess)
promess = operation.eval(feed_dict={source:zip(DATA_PER_KERNEL, [(0,0,0) for _ in DATA_PER_KERNEL])}, wait=False, sess=sess)

local_jobs_done_timeline = []
result_count = 0
old = -1
result_idx = 0
promess.result_idx = list(range(NB_KERNEL,NB_KERNEL*(NB_IT+1)))
print(promess.result_idx)
while result_count<NB_KERNEL*NB_IT:
    print(result_idx)
    other, result_idx = promess.getStatus()
    print("todo : ", other)
    print("done : ", result_idx)
    result_count = len(result_idx)
    if old!=result_count:
        local_jobs_done_timeline.append((time.time(), result_idx))
        old = result_count
    time.sleep(1)


result = promess.getResult()
data_dict = {"start_call" : [], "start_compute": [], "FLOPS": [], "end_compute": [], "end_call": []}

for idx in promess.result_idx:
    start_call = start_time
    start_compute = result[promess.result_idx.index(idx)][1][1]
    end_compute =  result[promess.result_idx.index(idx)][1][2]
    flops = result[promess.result_idx.index(idx)][1][0]
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
dataFrame.to_csv("./data.csv", index_label="idx")
#pickle.dump(dataFrame, open("data.pickle", "wb"))