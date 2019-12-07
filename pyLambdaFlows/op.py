from .dispenser import *
from .session import get_default_session, set_default_session, Session
from .tree import *
from .utils import isIterable
from .upload import Uploader
import os 
import progressbar
from .DynamoGesture import *
import json
from threading import Thread
import pickle
import traceback

class pyLambdaElement:
    def _send(self, uploader, purge=False):
        raise NotImplementedError()

    def _generate(self, tree, feed_dict=None):
        raise NotImplementedError()

class Source(pyLambdaElement):
    def __init__(self):
        self.parent = None
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.func_path = os.path.join(os.path.join(dir_path, "external"),"source.py")
        self.funct = os.path.join(os.path.join(dir_path, "external"),"source.py")

    def _send(self, uploader, purge=False):
        self.aws_lambda_name = uploader.upload_lambda(self.func_path, purge=purge)


    def _generate(self, tree, feed_dict=None):
        if feed_dict is None or feed_dict.get(self, None) is None:
            raise RuntimeError("Missing feed_dict values")
        tree.putRoot(self.aws_lambda_name, feed_dict[self])



class Operation(pyLambdaElement):
    def __init__(self, parent, funct, topologie, name=None):
        if isIterable(parent):
            if len(list(filter(lambda x : isinstance(x, pyLambdaElement), parent)))!=len(parent):
                raise AttributeError("You must provide  a pyLambdaElement inherited class as a parent.")
        else:
            if (not isinstance(parent, pyLambdaElement)):
                raise AttributeError("You must provide  a pyLambdaElement inherited class as a parent.")


        if isIterable(topologie):
            if len(list(filter(lambda x : isinstance(x, Dispenser), topologie)))!=len(topologie):
                raise AttributeError("You must provide  a Dispenser inherited class as a topologie arg.")
        else:
            if (not isinstance(topologie, Dispenser)):
                raise AttributeError("You must provide  a Dispenser inherited class as a topologie arg.")
        
        if isIterable(parent) and not isIterable(topologie):
            topologie = (topologie,)*len(parent)


        self.parent = parent if isIterable(parent) else [parent]
        self.funct = funct

        self.aws_lambda_name = None
        self.dispenser = topologie if isIterable(topologie) else [topologie]
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
        for par in self.parent:
            par._send(uploader, purge=purge)#TODO error
        
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
        
        tree = Tree(self)
        tree.compute(feed_dict)

        # Create dynamobd
        if not table_exists("pyLambda",sess):
            create_table("pyLambda",sess)
        fill_table("pyLambda", tree.gen_counter_values(), sess)
        put_entry("pyLambda", -1, [], 0, sess)

        # Create input json
        input_json = tree.generateJson(tableName="pyLambda")
        #return input_json
        # Launch 
        lambda_client = sess.getLambda()
        for _, request in progressbar.progressbar(input_json.items()):

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
            error = False
            err_list = list()
            while not receive and not error:
                res = get_data("pyLambda", i, sess=sess)
                receive = not res is None
                _, remaining, err_list =  get_entry("pyLambda", -1, sess)
                if remaining == 1:
                    error = True

            if error and len(err_list)>0:
                idx, etype, value, tb = err_list[0]
                output = ('{2}\n' +
                      '\nThe above exception was first raised by a AWS lambda instance (number '+ str(idx) +' linked  to op : '+str(tree.getNode(idx))+' ): \n' +
                      'Distant traceback :\n' +
                      '{0}' +
                      '{1}: {2}''').format(''.join(traceback.format_list(tb)), etype.__name__, str(value))
            
                raise etype(output)
                

        return res

    def _generate(self, tree, feed_dict=None):
        self.parent._generate(tree, feed_dict=feed_dict)
        tree.addLayer(self.aws_lambda_name, self.dispenser, name=self.name)
    
    def __str__(self):
        return "<{} op, funct: {}, name: {}>".format(self.__class__.__name__, self.funct, self.name)


class Map(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DMap(), name=name)


class Reduce(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DHardReduce(), name=name)

