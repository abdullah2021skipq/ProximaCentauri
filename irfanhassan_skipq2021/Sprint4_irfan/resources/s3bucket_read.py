import json
import boto3
#import constants as constant_

s3= boto3.client('s3')

class s3bucket_read:
    def __init__(self,bucketname, filename):
        self.Object = boto3.client('s3').get_object(Bucket=bucketname,Key=filename)
    
    def bucket_as_list(self  ):
        
        contetnt = self.Object['Body']
        json_oject = json.loads(contetnt.read())   #get dictionary
        list_url=list(json_oject.values())
       # for url in list_url:
       #     print(url)
       #     print('--------')
        return list_url