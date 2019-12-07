import os
import tempfile
import zipfile
import botocore
import hashlib
import warnings

from .version import __version__, __aws_python_version__

def getHash(fil, nb_digits=5):
    fil.seek(0)
    digest = hashlib.md5()
    digest.update(bytes(__version__, 'utf-8') + fil.read())
    res = digest.hexdigest()
    fil.seek(0)
    return res[0:nb_digits]

class Uploader:
    def __init__(self, sess):
        self.sess = sess
        iam_client = self.sess.getIAM()
        self.role = iam_client.get_role(RoleName='LambdaBasicExecution')
        self.already_pushed = {}

    def upload_lambda(self, funct_path, purge=False):
        if funct_path in self.already_pushed.keys():
            return self.already_pushed[funct_path]
        
        try:
            if os.path.basename(funct_path).split('.')[-1] != "py":
                raise RuntimeError("Your funct path must be a .py file")
        except Exception:
            raise RuntimeError("Your path isn't valid !")
        
        lambda_name = os.path.basename(funct_path).split('.')[0]

        
        f = tempfile.TemporaryFile()
        with zipfile.ZipFile (f, "a") as zipObj:
            zipObj.write(funct_path, os.path.basename(funct_path) )
            dir_path = os.path.dirname(os.path.realpath(__file__))
            zipObj.write(os.path.join(dir_path, "external","decorator.py"), os.path.join("pyLambdaFlows","decorator.py"))

        f.seek(0)

        lambda_name = lambda_name + '-' + getHash(f)

        lambda_client = self.sess.getLambda()
        #Look if lambda exist
        alreadyExist = False
        try:
            lambda_client.get_function(FunctionName=lambda_name)
            alreadyExist = True
        except lambda_client.exceptions.ResourceNotFoundException:
            pass
        
        if(alreadyExist):
            if(purge):
                warnings.warn("Lambda Already on AWS dataBase ({}), removing...".format(lambda_name), RuntimeWarning)
                lambda_client.delete_function(FunctionName=lambda_name)
            else:
                warnings.warn("Lambda Already on AWS dataBase ({})".format(lambda_name), RuntimeWarning)
                self.already_pushed[funct_path] = lambda_name
                return lambda_name

        #TODO catch error
        lambda_client.create_function(
            FunctionName=lambda_name,
            Runtime=__aws_python_version__,
            Role=self.role['Role']['Arn'],
            Handler=lambda_name.split("-")[0]+".lambda_handler",
            Code=dict(ZipFile=f.read()),
            Timeout=300, # Maximum allowable timeout
            )
        self.already_pushed[funct_path] = lambda_name
        return lambda_name