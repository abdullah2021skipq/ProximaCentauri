import botot3

def ReadFromTable(tableName)
    client = boto3.client('dynamodb')
    
    Urls = client.scan(
            TableName=tableName,
            AttributesToGet=[
            'Links'])
    
    return Urls 
