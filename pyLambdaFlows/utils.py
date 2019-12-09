from .DynamoGesture import get_entries

def isIterable(obj):
    try:
        _ = iter(obj)
    except TypeError:
        return False
    return True


class PromessResult():
    def __init__(self, table_name, result_idx, sess):
        self.result_idx = result_idx
        self.session = sess 
        self.table = table_name

    def getStatus(self):
        database_status = get_entries(self.table, min(self.result_idx), max(self.result_idx), sess=self.session)

        remaining = list(filter(lambda  element: element[1] is None, database_status))
        done = list(filter(lambda  element: not element[1] is None, database_status))
        return [element[0] for element in remaining], [element[0] for element in done]

    def getResult(self):
        table_data =  get_entries(self.table, min(self.result_idx), max(self.result_idx), sess=self.session)
        return [element[1] for element in table_data]