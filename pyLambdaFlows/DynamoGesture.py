import botocore 
from .session import get_default_session


def reset_table(table_name, sess=None):
    if sess is None:
        sess = get_default_session()
    # delete if exist
    delete_table(table_name, sess=sess)
    create_table(table_name, sess=sess)


def table_exists(table_name, sess=None):
    if sess is None:
        sess = get_default_session()
    client = sess.getDynamoDb()
    clientRessource = sess.getDynamoDbRessource()
    table = clientRessource.Table("pyLambda")
    try:
        table.table_status
    except client.exceptions.ResourceNotFoundException:
        return False
    return True


def delete_table(table_name, sess=None):
    if sess is None:
        sess = get_default_session()
    client = sess.getDynamoDb()
    clientRessource = sess.getDynamoDbRessource()
    while True:        
        try:
            table = clientRessource.Table(table_name)
            table.delete()
            table.wait_until_not_exists()
        except client.exceptions.ResourceInUseException:
            continue
        except client.exceptions.ResourceNotFoundException:
            break



def create_table(table_name, sess=None):
    if sess is None:
        sess = get_default_session()
    client = sess.getDynamoDb()
    clientRessource = sess.getDynamoDbRessource()

    table = clientRessource.Table(table_name)

    client.create_table(TableName=table_name,
        KeySchema=[ {
                    "AttributeName" : "id",
                    "KeyType" : "HASH"
                },
                {
                    "AttributeName" : "counter", 
                    "KeyType" : "RANGE"

                }],
        AttributeDefinitions=[
            {
                "AttributeName" : "id",
                "AttributeType" : "N"
            }, 
            {
                "AttributeName" : "counter",
                "AttributeType" : "N"
            }],
        ProvisionedThroughput={
            'ReadCapacityUnits' : 100,
            'WriteCapacityUnits' : 100
        })
    table.wait_until_exists()



def fill_table(table_name, counter_init, sess=None):
    if sess is None:
        sess = get_default_session()
    client = sess.getDynamoDb()
    for idx, init_val in enumerate(counter_init):
        client.put_item(TableName=table_name, Item={
            "id" : {"N" : str(idx)},
            "counter" : { "N" : str(init_val)}
        })
    return