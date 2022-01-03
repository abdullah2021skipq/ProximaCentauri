import boto3
from boto3.dynamodb.conditions import Key


class dynamodbPut:
    def __init__(self):
        self.resource = boto3.resource('dynamodb') 
    def dynamo_data(self, tableName, message, createdDate):
        table = self.resource.Table(tableName)
        values = {}
        values['id'] = message
        values['createdDate'] = createdDate
        table.put_item(Item = values)