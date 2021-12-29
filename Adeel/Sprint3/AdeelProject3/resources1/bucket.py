import boto3
import json


class Bucket():
    def __init__(self,buketname , key):
        self.Object = boto3.client('s3').get_object(Bucket=buketname,Key=key)
    def bucket_as_list(self  ):
        data = self.Object['Body']
        #data = Object['Body']
        jObj = json.loads(data.read())
        listUrl = list(jObj.values())
        return(listUrl)
        
        
