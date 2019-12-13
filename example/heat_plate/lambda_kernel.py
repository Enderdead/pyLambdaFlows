import time
from pyLambdaFlows.decorator import kernel
from random import random
import copy
@kernel
def lambda_handler(conv_map):
    left, mid, right = conv_map
    # Drop perf log 
    left = left[0]
    mid = mid[0]
    right = right[0]

    # Get only relevante data
    left = left[-1]
    right = right[0]

    # Copy mid
    result = copy.deepcopy(mid)

    t1 = time.time()
    if len(result)==1:
        for index in range(1,len(result[0])-1):
            result[0][index] = ((mid[0][index-1] + mid[0][index] + mid[0][index+1]) + 
                        (left[index-1] + left[index] + left[index+1]) + 
                        (right[index-1] + right[index] + right[index+1]))/9
        FLOPS = (len(result[0])-2)*10
    elif len(result)>1:
        FLOPS = 0
        #Left side
        for index in range(1,len(result[0])-1):
            result[0][index] = ((mid[0][index-1] + mid[0][index] + mid[0][index+1]) + 
                        (left[index-1] + left[index] + left[index+1]) + 
                        (mid[1][index-1] + mid[1][index] + mid[1][index+1]))/9
        FLOPS += (len(result[0])-2)*10 
        #Right side
        for index in range(1,len(result[0])-1):
            result[-1][index] = ((mid[-1][index-1] + mid[-1][index] + mid[-1][index+1]) + 
                        (mid[-2][index-1] + mid[-2][index] + mid[-2][index+1]) + 
                        (right[index-1] + right[index] + right[index+1]))/9
        FLOPS += (len(result[0])-2)*10 

        #Center
        for row_idx in range(1, len(result)-1):
            for index in range(1,len(result[0])-1):
                result[row_idx][index] = ((mid[row_idx][index-1] + mid[row_idx][index] + mid[row_idx][index+1]) + 
                            (mid[row_idx-1][index-1] + mid[row_idx-1][index] + mid[row_idx-1][index+1]) + 
                            (mid[row_idx+1][index-1] + mid[row_idx+1][index] + mid[row_idx+1][index+1]))/9

            FLOPS += (len(result[0])-2)*10 

    else:
        raise RuntimeError("Bad grid format")

    t2 = time.time()

    return result, (FLOPS, t1, t2)
