import boto3

from boto3.dynamodb.conditions import Key

import os
class dynamoTablePutData:
    def __init__(self):
        self.resource = boto3.resource('dynamodb') 
    def dynamo_data(self, tableName, message, createdDate):
        table = self.resource.Table(os.getenv('TABLE_NAME'))
        print(os.getenv('TABLE_NAME'))
        values = {}
        values['id'] = message
        values['createdDate'] = createdDate
        #values['Reason'] = reason
        table.put_item(Item = values)
