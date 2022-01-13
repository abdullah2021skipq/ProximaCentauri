from __future__ import print_function
import boto3
import json

def lambda_handler(event, context):
    dynamodbTable = boto3.resource('dynamodb').Table('waheeds3table')
    api_menu = event['params']['path']['URL_ADDRESS']

    result = dynamodbTable.get_item(
        Key={
            'url': api_menu
        }
        )

    # create a response
    response = {
        "body": result['Item']
    }

    return response