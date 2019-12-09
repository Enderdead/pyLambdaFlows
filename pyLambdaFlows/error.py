
class NoSessionGiven(RuntimeError):
    """
    This error is risen with any session can be found (neither default way nor specified way).
    """
    def __init__(self, message=None):
        if message is None:
            RuntimeError.__init__(self, "No session can be found (You can provide it with the kwargs sess or with a default one)")
        else:
            RuntimeError.__init__(self, message)