#s3bucket_url

#s3bucket_url
import json
import boto3


def read_url_list(bucket_talha,file_name):
    s3= boto3.client('s3')
    #bucket_talha= "talhabucketnew"
    #file_name ="URLS_new.json"
    response= s3.get_object(Bucket=bucket_talha ,Key=file_name)
    cont = response['Body']
    json_oject = json.loads(cont.read())
    list_url= list(json_oject.values())# [json_oject['w1'],json_oject['w2'],json_oject['w3'],json_oject['w4']]
    return list_url
        
