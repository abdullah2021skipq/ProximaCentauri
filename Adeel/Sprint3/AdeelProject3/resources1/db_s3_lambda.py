import boto3,os

from bucket import Bucket as bo 

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    
    ####################boto 3 client##############
    
    
    client = boto3.client('dynamodb')
    
    #################### S3 event ########################
    
    BucketName = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(str(event))
    print(key)
    print(BucketName)
    
    ################## taking bucket and converting them in list################
    
    Url_Monitor= bo(BucketName,key).bucket_as_list()
    print(Url_Monitor)
    
    ###################### table name #######################
    
    name = os.getenv('table_name')#getting table name
    print(name)
    
    
    ###################### puting urls in table ###############
    
    for link in Url_Monitor:
        client.put_item(
        TableName = name,
        Item={'Links':{'S': link}
        })
    return 'Successfully Added Urls in Dynamo'