

def isIterable(obj):
    try:
        _ = iter(obj)
    except TypeError:
        return False
    return True