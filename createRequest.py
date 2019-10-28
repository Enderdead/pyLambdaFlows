"""
File for json making. Create Json for all lambda process and subprocess
"""
from loadData import DATA
from copy import deepcopy

def createRequest(buketName="moyenne"):
    ResquestMoyen = list()

    for idx, data in DATA.items():
        batchDict = dict()
        batchDict["idx"] = idx 
        batchDict["data"] = deepcopy(data)
        batchDict["bucket"] = buketName 
        del batchDict["data"]["id"]
        #batchDict["nextEvent"] = (None, None)
        ResquestMoyen.append(batchDict)

    ResquestMoyen[0]["nextEvent"] = ["ClassMean", {"idx": '32', 'bucket':buketName,'data':[str(i) for i in range(0,16,1)], 'nextEvent': ["MeanEta", {"idx":"34",'bucket':buketName, "data": ["32","33"]}] }]

    ResquestMoyen[16]["nextEvent"] = ["ClassMean", {"idx": '33', 'bucket':buketName,'data':[str(i) for i in range(16,32,1)] }] # 'nextEvent'(None,None)

    return ResquestMoyen

if __name__ == "__main__":
    print(createRequest())