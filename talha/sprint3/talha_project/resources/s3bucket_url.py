#s3bucket_url
import json
import boto3


def write_urls_to_table(tablename):
    s3= boto3.client('s3')
    bucket_talha= "talhabucketnew"
    file_name ="URLS_new.json"
    response= s3.get_object(Bucket=bucket_talha ,Key=file_name)
    cont = response['Body']
    json_oject = json.loads(cont.read())
    list_url=[json_oject['w1'],json_oject['w2'],json_oject['w3'],json_oject['w4']]
    
    resource= boto3.resource('dynamodb')
    table = resource.Table(tablename)
    for el in list_url:
        values = {}
        values['URL'] = el
        table.put_item(Item = values)

    
def read_url_list_from_table(tablenamee):
    resource= boto3.resource('dynamodb')
    table = resource.Table(tablenamee)
    table.get_item(Key={"partition_key":"URL"})

    response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data