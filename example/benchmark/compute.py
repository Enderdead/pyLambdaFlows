import time
from pyLambdaFlows.decorator import kernel
from random import random

@kernel
def lambda_handler(inputData):
    loopcount, MAT_N = inputData
    A = list()
    B = list()
    C = list()

    for i in range(MAT_N):

        line_A = list()
        line_B = list()
        line_C = list()

        for j in range(MAT_N):
            line_A.append(random())
            line_B.append(random())
            line_C.append(0.)
        A.append(line_A)
        B.append(line_B)
        C.append(line_C)
    
    t1 = time.time()
    for _ in range(loopcount):
        for i in range(MAT_N):
            for j in range(MAT_N):
                for k in range(MAT_N):
                    C[i][j] += A[i][k]*B[k][j]


    FLOPS = loopcount * MAT_N**3 
    t2 = time.time()
    return FLOPS / (t2-t1), t1, t2