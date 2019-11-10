from .dispenser import *
from .session import get_default_session, set_default_session, Session
from .utils import *
from .upload import Uploader

class pyLambdaElement:
    def _send(self, sess):
        raise NotImplementedError()

    def _generate(self, tree, feed_dict=None):
        raise NotImplementedError()



class Source(pyLambdaElement):
    def __init__(self):
        pass

    def _send(self, sess):
        pass

    def _generate(self, tree, feed_dict=None):
        if feed_dict is None or feed_dict.get(self, None) is None:
            raise RuntimeError("Missing feed_dict values")

        tree.putRoot(None, feed_dict[self])



class Operation(pyLambdaElement):
    def __init__(self, parent, funct, topologie, name=None):
        if(not isinstance(parent, pyLambdaElement)):
            raise AttributeError("You must provide  a pyLambdaElement inherited class as a parent")

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
        """
            send source code 
        """

        self.parent._send(sess)
        
        #TODO send to AWS using sess
        if self.name is None:
            print("send {} to AWS !".format(self.funct))
        else: 
            print("{} : send {} to AWS !".format(self.name, self.funct))

    def eval(self, feed_dict=None, sess=None):
        " Call this operation (generate the json data)"

        if sess is None:
            sess = get_default_session(check_if_none=True)
        else:
            if not isinstance(sess, Session):
                raise RuntimeError("You must provide a Session object as sess kwarg.")
        
        tree = Tree()
        self._generate(tree, feed_dict=feed_dict)

        # Create input json
        input_json = tree.generateJson()

        # Get all lamnda to create
        functions_list = tree.getfunctList()

        # TODO hash to not recreate function

        # Upload functions
        upload = Uploader(sess)
        for function in functions_list :
            upload.upload_lambda(function)



    def _generate(self, tree, feed_dict=None):
        self.parent._generate(tree, feed_dict=feed_dict)
        tree.addLayer(self.funct, self.dispenser, name=self.name)
            

class Map(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DMap(), name=name)


class Reduce(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DHardReduce(), name=name)

