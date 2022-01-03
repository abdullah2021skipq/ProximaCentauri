import json
import boto3
#import constants as constant_

s3= boto3.client('s3')

class s3bucket_read:
    def __init__(self):
        self.Object = boto3.client('s3').get_object(Bucket="irfanskipq",Key="URL.json")
    
    def bucket_as_list(self  ):
        response= s3.get_object(Bucket="irfanskipq",Key="URLS.json")
        contetnt = response['Body']
        json_oject = json.loads(contetnt.read())   #get dictionary
        list_url=[json_oject['link1'],json_oject['link2'],json_oject['link3'],json_oject['link4']]
        for url in list_url:
            print(url)
            print('--------')
        
        return list_url