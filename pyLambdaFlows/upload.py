import os
import tempfile
import zipfile

class Uploader:
    def __init__(self, sess):
        self.sess = sess
        iam_client = self.sess.getIAM()
        self.role = iam_client.get_role(RoleName='LambdaBasicExecution')

    def upload_lambda(self, funct_path):
        try:
            if os.path.basename(funct_path).split('.')[-1] != "py":
                raise RuntimeError("Your funct path must be a .py file")
        except Exception:
            raise RuntimeError("Your path isn't valid !")
        
        lambda_name = os.path.basename(funct_path).split('.')[0]

                
        f = tempfile.TemporaryFile()
        with zipfile.ZipFile (f, "a") as zipObj:
            zipObj.write("./test.py", "test.py" )
        f.seek(0)

                # Remove if lambda already exist
        lambda_client = self.sess.getLambda()

        try:
            lambda_client.delete_function(FunctionName=lambda_name)
        except:
            pass

        lambda_client.create_function(
            FunctionName=lambda_name,
            Runtime='python3.7',
            Role=self.role['Role']['Arn'],
            Handler=lambda_name+".lambda_handler",
            Code=dict(ZipFile=f.read()),
            Timeout=300, # Maximum allowable timeout
            )