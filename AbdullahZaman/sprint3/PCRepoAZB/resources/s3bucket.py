import boto3
import json

def store_file(buck):
    s3= boto3.client('s3')
    try:
        s3.create_bucket(Bucket=buck, CreateBucketConfiguration={       # creating our s3 bucket and storing file
        'LocationConstraint': 'us-east-2'})
        s3.upload_file("resources/urls.json", buck ,"urlsList.json")
    except:
        s3.upload_file("resources/urls.txt", buck ,"urlsList.json")
        

def read_file(buck, item):
    name_url = []
    s3 = boto3.client('s3').get_object(Bucket=buck, key=item)
    obj = s3['Body']
    obj = json.loads(obj.read())        # .loads return a dictionary
    return list(obj.values())