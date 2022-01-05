import boto3

def getting_sprint3_dynamo_data():
    items_list = []
    client_ = boto3.client('dynamodb')
    items = client_.scan(TableName="AbdullahSprint3")
    items = items["Items"]
    for item in items:
        item = item["URL_ADDRESS"]['S']
        items_list.append(item)
    
    return items_list
    

print(getting_sprint3_dynamo_data())
