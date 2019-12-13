import time
from pyLambdaFlows.decorator import kernel
from random import random

@kernel
def lambda_handler(conv_map):
    left, mid, right = conv_map
    left = left[0]
    mid = mid[0]
    right = right[0]
    result = [element for element in mid]

    t1 = time.time()
    for index in range(1,len(result)-1):
        result[index] = ((mid[index-1] + mid[index] + mid[index+1]) + 
                     (left[index-1] + left[index] + left[index+1]) + 
                     (right[index-1] + right[index] + right[index+1]))/9
    FLOPS = (len(result)-2)*10
    t2 = time.time()

    return result, FLOPS / (t2-t1), t1, t2
