import constants
import boto3
import dynamo_db


def lambda_database_function(event,context):
    
    
    timestamp= str(event['Records'][0]["Sns"]["Timestamp"])
    message= str(event['Records'][0]["Sns"]["Message"])
    response=dynamo_db.put_event_data(timestamp,message)
    return response
    
 
