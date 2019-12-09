import pickle
from .utils import isIterable



class Tree():
    def __init__(self, target):
        self.depth = 0 
        self.max_idx = 0
        self.target = target
        
        self.aws_functions = set()
        
        self.bottoms = list()
        
        self.treated = dict()

    def compute(self, feed_dict):
        self.aws_functions = set()
        self.bottoms = list()
        self.treated = dict()
        self.curr_idx = 0
        self.dfs(self.target, feed_dict)
        self.max_idx = self.curr_idx

    def dfs(self, node, feed_dict):
        if node.parent is None:
            # We are in a leaf
            if not node in feed_dict:
                raise RuntimeError("Some source op don't have provided values !")
            
            lambda_list = list()
            for element in feed_dict[node]:
                lambda_list.append(InstanceNode(node.funct, pickle.dumps(element).hex(), self.curr_idx, None))
                self.curr_idx += 1
            self.treated[node] = lambda_list
            return 

        for parent in node.parent:
            if not parent in self.treated: 
                self.dfs(parent, feed_dict)
        
        dependencies = list()
        for idx, parent in enumerate(node.parent):
            dependencies.append(node.dispenser[idx](len(self.treated[parent])))

        if len(set(map(lambda x: len(x), dependencies)))>1:
            raise RuntimeError("Node get multiple parent with differents dim !")

        lambda_list = list()
        # If we have only one parent, we will have a 1dim data field
        if(len(dependencies)==0):
            raise RuntimeError("Intern Eror")
        elif(len(dependencies)==1):
            dependencies = dependencies[0]
            for dep in dependencies:
                curr_parents = list()
                for element in dep:
                    curr_parents.append(self.treated[node.parent[0]][element])
                lambda_list.append(InstanceNode(node.funct, None, self.curr_idx, curr_parents))
                self.curr_idx+=1

        # If we have mult-parent, we shall get a 2 dim data field
        else:
            for dep in zip(*dependencies):
                curr_parents = list()
                for i in range(len(dep)):
                    sub_curr_parents= list()
                    for sub in dep[i]:
                        sub_curr_parents.append(self.treated[node.parent[i]][sub])
                    curr_parents.append(sub_curr_parents)

                lambda_list.append(InstanceNode(node.funct, None, self.curr_idx, curr_parents))
                self.curr_idx+=1
        self.treated[node] = lambda_list

    def getNode(self, idx):
        for key, items in self.treated.items():
            if len(list(filter(lambda x: x.idx==int(idx), items)))>0:
                return key
        return None

    def generateJson(self, tableName="None"):
        jsonData = dict()

        BFS_queue = [self.target]

        while len(BFS_queue)!=0:
            curr_node = BFS_queue[0]
            del BFS_queue[0]
            if not curr_node.parent is None:
                for par in curr_node.parent:
                    BFS_queue.append(par)
                    
            for element in self.treated[curr_node]:
                curr_json = dict()
                curr_json["idx"] = str(element.idx)
                curr_json["func"] = curr_node.aws_lambda_name
                curr_json["children"] = element.childrenJson
                curr_json["data"] = list()
                curr_json["table"] = tableName

                if not element.parents is None:
                    curr_json["source"] = "data"

                    # TODO python use ref so we can gather those loop but I have to be sure
                    for parent in element.parents:
                        if isIterable(parent):
                            curr_json["data"].append(list(map(lambda element: str(element.idx),parent)))
                        else:
                            curr_json["data"].append(str(parent.idx))
                    for parent in element.parents:    
                        if isIterable(parent):
                            for sub_parent in parent:
                                sub_parent.add_children_data(str(element.idx), curr_json)
                        else:
                            parent.add_children_data(str(element.idx), curr_json)

                else:
                    curr_json["source"] = "direct"
                    curr_json["data"].append(element.args) 
                    jsonData[element.idx] = curr_json
        return jsonData

    def gen_counter_values(self):
        result = [0,]*self.curr_idx
        for elements_list in self.treated.values():
            for element in elements_list:
                if not element.parents is None :
                    result[element.idx] = len(element.parents)
        return result
        
    def getResultIdx(self):
        return [ element.idx for element in self.treated[self.target] ]

class InstanceNode():
    def __init__(self, funct, args, idx, parents=None):
        self.funct = funct # Path function
        self.args = args # Equals data if root or None otherwise
        self.idx = idx # idx
        self.parents = parents
        self.childrenJson = dict()

    def add_children_data(self, idx, json):
        self.childrenJson[idx] = json

