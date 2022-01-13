import pytest
import requests
import boto3
url_table="BetaStag-irfanskipqstack-irfanurltableF418808E-1WH3K1DY935ZF"
################# test 1 to check put method is working in api #########################################
def test_apigateway():
    url="www.test.com"
    api_test = requests.put('https://hwmcjcc01f.execute-api.us-east-2.amazonaws.com/prod/',data = url)
    url_list=read_table()
    ans=True
    if url not in url_list:
        ans=False
    assert ans   
############### test 2 to check delete method is working in API ########################################
def test_apigateway_delete():
    url="www.test.com"
    api_test = requests.delete('https://hwmcjcc01f.execute-api.us-east-2.amazonaws.com/prod/',data = url)
    url_list=read_table()
    ans=True
    if url in url_list:
        ans=False
    assert ans

############# function to read url from table ##########################################################
def read_table():
    client = boto3.client('dynamodb')
    table_data = client.scan(TableName=url_table,AttributesToGet=['URL'])
    url_list=table_data["Items"]
    for n in range(len(url_list)):
            url_list[n]=url_list[n]['URL']['S']
    return url_list
