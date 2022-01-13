
import json
import boto3
import json
def read_buk(buc, item):
    s3 = boto3.client('s3').get_object(Bucket=buc, Key=item)
    obj = s3['Body']
    obj = json.loads(obj.read())
    urllist = list(obj.values())
    return (urllist)