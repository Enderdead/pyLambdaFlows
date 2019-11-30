class Tree():
    def __init__(self):
        self.depth = 0 
        self.layers = list()
        self.max_idx = 0

    def putRoot(self, funct, data):
        root = list()
        for idx, element in enumerate(data):
            root.append(InstanceNode(funct, element, idx, parents=None))
        self.layers.append(root)
        self.depth +=1

    def addLayer(self, funct, topologie, name=None):
        layer = list()
        last_idx = self.layers[-1][-1].idx + 1
        distribution = topologie(len(self.layers[-1]))
        for idx, dependancies in enumerate(distribution):
            parents = list()
            for dep in dependancies:
                parents.append(self.layers[-1][dep])
            layer.append(InstanceNode(funct, None, idx+last_idx, parents=parents))
        self.layers.append(layer)
        self.max_idx = last_idx + len(layer)
        self.depth +=1

    def getfunctList(self):
        result = set()
        for layer in self.layers:
            if not layer[0].funct is None:
                result.add(layer[0].funct)
        return list(result)


    def generateJson(self, bucket_name="None"):
        jsonData = dict()
        curr_depth = len(self.layers)-1
        while curr_depth!=-1:
            for element in self.layers[curr_depth]:
                curr_json = dict()
                curr_json["idx"] = str(element.idx)
                curr_json["func"] = element.funct
                curr_json["children"] = element.childreJson
                curr_json["data"] = list()
                curr_json["bucket"] = bucket_name

                if not element.parents is None:
                    curr_json["source"] = "data"
                    # TODO remove this later with dynamo db
                    first_one=True
                    for parent in element.parents:
                        curr_json["data"].append(str(parent.idx))
                        if first_one:
                            parent.add_children_data(str(element.idx), curr_json)
                            first_one = False

                else:
                    curr_json["source"] = "direct"
                    curr_json["data"].append(str(element.args))

                
                if(curr_depth==0):
                    jsonData[element.idx] = curr_json
            curr_depth -= 1
        return jsonData



class InstanceNode():
    def __init__(self, funct, args, idx, parents=None):
        self.funct = funct # Path function
        self.args = args # Equals data if root or None otherwise
        self.idx = idx # idx
        self.parents = parents
        self.childreJson = dict()

    def add_children_data(self, idx, json):
        self.childreJson[idx] = json