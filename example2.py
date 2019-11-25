import pyLambdaFlows
import boto3
sess = pyLambdaFlows.Session(credentials_csv="./accessKeys.csv")


#pyLambdaFlows.DynamoGesture.delete_table("pyLambda", sess=sess)

#pyLambdaFlows.DynamoGesture.create_table("pyLambda", sess=sess)
#pyLambdaFlows.DynamoGesture.delete_table("pyLambda", sess=sess)
print("fin")
#pyLambdaFlows.DynamoGesture.delete_table("pyLambda", sess=sess)

#pyLambdaFlows.DynamoGesture.fill_table("pyLambda", [1, 2, 3], sess=sess)
res = pyLambdaFlows.DynamoGesture.decremente("pyLambda", 1, sess=sess)
#a = boto3.resource("dynamodb", region_name=sess.region, aws_access_key_id=sess.aws_access_key_id, aws_secret_access_key= sess.aws_secret_access_key)
#table = a.Table("pyLambda")


