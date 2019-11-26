

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

def decorate(func):
#Le wrapper permet d'acceder aux arguments de la function decore
    def wrapper(event, context):
        a = list(args)
        #pre traitement
        # Get all event data
        idx   = event["idx"]
        source = event["source"]
        data = event["data"]
        children = event["children"]
        bucket = event["bucket"]
        
        inputData = list()
        if(source=='direct'):
            inputData = [int(element) for element in data]
        if(source=='data'):
            S3Client = boto3.client('s3')
            for idx_loc in data:
                batchResult = None
                while batchResult is None:
                    try:
                        batchResult = pickle.loads(S3Client.get_object(Bucket=bucket, Key=idx_loc)["Body"].next())
                    except:
                        sleep(0.2)
                        continue
                inputData.append(batchResult)     
        #execution du code
        reponse = func(inputData)
        #post traitement
        # Store
        S3Client = boto3.client('s3')
        S3Client.put_object(Body = pickle.dumps(inputData), Bucket=bucket, Key=idx)

        # Treatment
        if(len(children.keys()) != 0):
            for _, item in children.items():
                lambda_client = boto3.client('lambda')

                lambda_client.invoke(
                FunctionName=item['func'],
                InvocationType='Event',
                Payload=json.dumps(item),
                )
    return {
        'statusCode': 200,
        'body': json.dumps("Ok")
        }   
return decorate



class InstanceNode():
    def __init__(self, funct, args, idx, parents=None):
        self.funct = funct # Path function
        self.args = args # Equals data if root or None otherwise
        self.idx = idx # idx
        self.parents = parents
        self.childreJson = dict()

    def add_children_data(self, idx, json):
        self.childreJson[idx] = json