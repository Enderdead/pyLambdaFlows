from .dispenser import *
from .session import get_default_session, set_default_session, Session
from .utils import *
from .upload import Uploader
import os 
import progressbar
from .DynamoGesture import *
import json
from threading import Thread
import pickle
class pyLambdaElement:
    def _send(self, uploader, purge=False):
        raise NotImplementedError()

    def _generate(self, tree, feed_dict=None):
        raise NotImplementedError()

class Source(pyLambdaElement):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.func_path = os.path.join(os.path.join(dir_path, "external"),"source.py")

    def _send(self, uploader, purge=False):
        self.aws_lambda_name = uploader.upload_lambda(self.func_path, purge=purge)


    def _generate(self, tree, feed_dict=None):
        if feed_dict is None or feed_dict.get(self, None) is None:
            raise RuntimeError("Missing feed_dict values")
        tree.putRoot(self.aws_lambda_name, feed_dict[self])



class Operation(pyLambdaElement):
    def __init__(self, parent, funct, topologie, name=None):
        if(not isinstance(parent, pyLambdaElement)):
            raise AttributeError("You must provide  a pyLambdaElement inherited class as a parent")

        self.parent = parent
        self.funct = funct

        self.aws_lambda_name = None
        if(not isinstance(topologie, Dispenser)):
            raise AttributeError("You must provide  a Dispenser inherited class as a topologie arg")
        
        self.dispenser = topologie
        self.name = name

    def compile(self, sess=None, purge=False):
        " This function send this lambda op in AWS service"
        if sess is None:
            sess = get_default_session(check_if_none=True)
        else:
            if not isinstance(sess, Session):
                raise RuntimeError("You must provide a Session object as sess kwarg.")
        
        # Upload functions
        upload = Uploader(sess)
        self._send(upload, purge=purge)



            
    def _send(self, uploader, purge=False):
        """
            send source code 
        """

        self.parent._send(uploader, purge=purge)
        
        #TODO send to AWS using sess
        if self.name is None:
            print("send {} to AWS !".format(self.funct))
        else: 
            print("{} : send {} to AWS !".format(self.name, self.funct))

        self.aws_lambda_name = uploader.upload_lambda(self.funct, purge=purge)
        if purge:
            uploader.sess.add_func_to_purge(self.aws_lambda_name)


    def eval(self, feed_dict=None, sess=None):
        " Call this operation (generate the json data)"

        if sess is None:
            sess = get_default_session(check_if_none=True)
        else:
            if not isinstance(sess, Session):
                raise RuntimeError("You must provide a Session object as sess kwarg.")
        
        tree = Tree()
        self._generate(tree, feed_dict=feed_dict)

        # Create bucket
        #create_bucket("pylambdaflows", tree.max_idx, sess)

        # Create dynamobd
        if not table_exists("pyLambda",sess):
            create_table("pyLambda",sess)
        fill_table("pyLambda", tree.gen_counter_values(), sess)

        # Create input json
        input_json = tree.generateJson(bucket_name="pylambdaflows")
        #return input_json
        # Launch 
        lambda_client = sess.getLambda()
        for idx, request in progressbar.progressbar(input_json.items()):

            def lol():
                lambda_client.invoke(
                    FunctionName=request["func"],
                    InvocationType='Event',
                    Payload=json.dumps(request),
                )
            Thread(target=lol).start()

        print("Computation got started ! ")
        res = None
        for i in progressbar.progressbar(range(0,tree.max_idx)):

            receive= False
            while not receive:
                res = get_data("pyLambda", i, sess=sess)
                receive = not res is None
        
        return res

    def _generate(self, tree, feed_dict=None):
        self.parent._generate(tree, feed_dict=feed_dict)
        tree.addLayer(self.aws_lambda_name, self.dispenser, name=self.name)
            


class Map(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DMap(), name=name)


class Reduce(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DHardReduce(), name=name)

