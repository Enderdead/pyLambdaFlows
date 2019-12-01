import boto3
import json
from time import sleep
import pickle
import decimal


def put_data(client, table_name, indexData, obj):
    table = client.Table(table_name)
    response = table.update_item(Key={
        'id' : int(indexData)
    },
    UpdateExpression="set #data = :val",
    ExpressionAttributeValues={
        ':val' : pickle.dumps(obj)
    },
    ExpressionAttributeNames={
    "#data": "data"
    },
    ReturnValues="UPDATED_NEW")


def get_data(client, table_name, indexData):
    return pickle.loads(client.get_item(TableName=table_name, Key= { "id" : {"N" : str(indexData)}})["Item"]["data"]["B"])


def kernel(func):
#Le wrapper permet d'acceder aux arguments de la function decore
    def wrapper(event, context):
        #pre traitement
        # Get all event data
        idx   = event["idx"]
        source = event["source"]
        data = event["data"]
        children = event["children"]
        dynamodb_table = event["table"]


        dynamoDbClient = boto3.client('dynamodb')
        dynamoDbRessource = boto3.resource('dynamodb')

        if(source=='direct'):
            inputData = [pickle.loads(bytes(bytearray.fromhex(element))) for element in data]
        if(source=='data'):
            inputData = list()
            for idx_loc in data:
                batchResult = get_data(dynamoDbClient, dynamodb_table, idx_loc)
                inputData.append(batchResult)   
        #execution du code
        result = func(inputData)
        #post traitement
        # Store
        put_data(dynamoDbRessource, dynamodb_table, idx, result)

        # Treatment
        if(len(children.keys()) != 0):

            for _, item in children.items():
                # Decremente 

                client = boto3.resource("dynamodb")
                table = client.Table(dynamodb_table)
                response = table.update_item(Key={
                    'id' : int(item["idx"])
                },
                UpdateExpression="set remaining = remaining - :val",
                ExpressionAttributeValues={
                    ':val' : decimal.Decimal(1)
                },
                ReturnValues="UPDATED_NEW")
                child_remaining_it = int(response["Attributes"]["remaining"])

                # call
                if child_remaining_it==0:
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
    return wrapper