
import json
import boto3
import json
class mywahedbuks3():
    def __init__(self):
        self.Object = boto3.client('s3').get_object(Bucket='waheedbuc',Key='urls.json')
    def bucket_as_list(self  ):
        data = self.Object['Body']
        jObj = json.loads(data.read())
        listUrl = list(jObj.values())
        return(listUrl) 