import pytest,requests , datetime,boto3,json
from resources1 import constants1 as constants
import resources1.db_ReadWrite_handler as dynamo_RW

client = boto3.client('dynamodb')
def test_ineg_put():
    case = False
    api_put = requests.put('http://2h8y18tiv9.execute-api.us-east-2.amazonaws.com/prod/',data = 'www.test.com')
    links = dynamo_RW.ReadFromTable(constants.URLS_TABLE_NAME)
    if 'www.test.com' in links:
        case = True
    assert case
    
def test_ineg_delete():
    case1 = False
    api_delete = requests.delete('http://2h8y18tiv9.execute-api.us-east-2.amazonaws.com/prod/',data = 'www.test.com')
    links = dynamo_RW.ReadFromTable(constants.URLS_TABLE_NAME)
    if 'www.test.com' not in links:
        case1 = True
    assert case1

''''
def test_ineg_get():
    case2 = 0
    api_get = requests.get('http://2h8y18tiv9.execute-api.us-east-2.amazonaws.com/beta/')
    res = json.loads(api_get.text)
    body = res['body']
    links = dynamo_RW.ReadFromTable(constants.URLS_TABLE_NAME)
    
    for item in links:
        if item in str(res):
            case2 = case2+1
    assert case2 == 4
'''