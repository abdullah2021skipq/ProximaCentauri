import boto3
from boto3.dynamodb.conditions import Key

import os
class dynamoTablePutURLData:
    def __init__(self):
        self.resource = boto3.resource('dynamodb') 
    def wdynamo_data(self, tableName, message):
        #db=boto3.client('dynamodb')
        table = self.resource.Table(tableName)
        values = {}
        values['URL'] = message
        #values['Reason'] = reason
        table.put_item(Item = values)
    #    db.put_item(tableName,Item = values)
    def rdynamo_data(self,tableName):
        dynamodb = boto3.resource('dynamodb')
        table = self.resource.Table(tableName)
#        table = dynamodb.Table(tableName)
        response = table.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data
    #Function for dynamodb table to delete an element
    def ddynamo_data(self,tableName,message):
        dynamodb = boto3.resource('dynamodb')
        table = self.resource.Table(tableName)
        #table = self.client.Table(tableName)
        response = table.delete_item(Key={'URL': message})
        return response
    
    
    #The end