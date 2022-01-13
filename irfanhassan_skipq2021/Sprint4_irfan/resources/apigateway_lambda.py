import boto3
import os
import json
from tablescan import tablescan 

########## lambda function will triger when user request any method using API Gateway ##################################
def lambda_handler(event,context):
    value = dict()
    dbscan=tablescan()
    client = boto3.client('dynamodb')
    #print(event)
    tablename = os.getenv('table_name')
    ### getting method name from event ###############################################################
    operation=event["httpMethod"]      #getting operation name from API Gatway request.
    #print(operation)
    #print(url)
    response=""

########### code for put item in url table ################################################################################    
    #https://dynobase.dev/dynamodb-python-with-boto3/#:~:text=To%20get%20all%20items%20from,the%20results%20in%20a%20loop
    if operation=="PUT":
        url=event['body']
        url_list=dbscan.read_table(tablename)
        if url not in url_list:
            client.put_item(TableName= tablename,Item={'URL':{'S' : url}})
            response="The item has been successfully putted into DynamoDB table."
        else:
            response="Failed to PUT: The Item is already available in DynamoDB table."
########### code for delete item in url table ################################################################################  
    elif operation=="DELETE":
        url=event['body']
        url_list=dbscan.read_table(tablename)
        if url in url_list:       #if item exist in table
            client.delete_item(TableName= tablename,Key={'URL':{'S' : url}}) #https://stackoverflow.com/questions/64187825/how-to-delete-all-the-items-in-the-dynamodb-with-boto3
            response="The item has been successfully deleted from DynamoDB table."
        else:                    #if item not exist.
            response="Failed to delete: The Item is not available in DynamoDB table."

########### code for get items in url table ###############################################################################################  
    elif operation=="GET":
        url_list=dbscan.read_table(tablename)
        response=url_list
        
########### code for update item in url table ################################################################################  
    elif operation=="POST":
        url=event['body']
        url_find=url.split(",")
        old_url=url_find[0]
        new_url=url_find[1]
        url_list=dbscan.read_table(tablename)  #read table
        if old_url in url_list:                 #if item is avaialble then 
            client.delete_item(TableName= tablename,Key={'URL':{'S' : old_url}})
            client.put_item(TableName= tablename,Item={'URL':{'S' : new_url}})
            response="The item has been successfully updated from DynamoDB table."
        else:                                   #incase item is not avaialble in table
            response="Failed to update: The Item is not available in DynamoDB table."
    
########### code for wrong selection ################################################################################      
    else:
        response="invalid request."
    
  
    return {'statusCode':200,
    'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': '*'
          },
    'body':json.dumps(response)}   
    
    
    

        
        