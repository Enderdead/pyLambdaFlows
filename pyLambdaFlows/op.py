from .dispenser import *
from .session import get_default_session, set_default_session, Session


class Source():
    pass


class Operation():
    def __init__(self, parent, funct, topologie, name=None):
        self.terminal = not isinstance(parent, Operation)
        self.parent = parent
        self.funct = funct

        if(not isinstance(topologie, Dispenser)):
            raise AttributeError("You must provide  a Dispenser inherited class as a topologie arg")
        
        self.dispenser = topologie
        self.name = name

    def compile(self, sess=None):
        " This function send this lambda op in AWS service"
        if sess is None:
            sess = get_default_session(check_if_none=True)
        else:
            if not isinstance(sess, Session):
                raise RuntimeError("You must provide a Session object as sess kwarg.")
        
        self._send(sess)
            
    def _send(self, sess):
        if not self.terminal:
            self.parent._send(sess)
        
        #TODO send to AWS using sess
        if self.name is None:
            print("send {} to AWS !".format(self.funct))
        else: 
            print("{} : send {} to AWS !".format(self.name, self.funct))

    def eval(self, sess=None):
        " Call this operation"

        if sess is None:
            sess = get_default_session(check_if_none=True)
        else:
            if not isinstance(sess, Session):
                raise RuntimeError("You must provide a Session object as sess kwarg.")
        pass

class Map(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DMap(), name=name)


class Reduce(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DHardReduce(), name=name)

