import json,os
import puturlDB as putdb
def lambda_handler(events, context):
 print(events)
 db=putdb.dynamoTablePutURLData()
 opt=events['httpMethod']
 path=events['path']
 table_name= os.environ['tablesname']
 msg=""
 if opt=='PUT':          ######///////PUT////////
  urls=events['body']#.split()
  #for url in urls:
  db.wdynamo_data(table_name,urls)
  msg="The item has been successfully written."
 elif opt=='GET':        ######////////GET///////
  urllist=db.rdynamo_data(table_name)
  msg="Your request is acknowledged"
  events['body']=urllist 
 elif opt=='DELETE':     ######///////DELETE///////
  urltodel=events['body']
  response=db.ddynamo_data(table_name,urltodel)
  msg="The Url has been deleted. Use GET method to check!"
 elif opt=='POST':        ######////////UPDATE///////
  exurl=events['body'].split(',')[0]
  replacewith=events['body'].split(',')[1]
  db.wdynamo_data(table_name,replacewith)
  db.ddynamo_data(table_name,exurl)
  msg= f"UPDATED: The URl, {exurl} is replaced with the new URL i.e {replacewith}."
 else: 
  msg="Please select an appropriate option. Appropriate Options=[PUT, GET, DELETE]"
 #if opt=='PUT' or opt=='DELETE':
  #urldict=db.rdynamo_data(table_name)#returns a dictionary
  #db.Newcreate_alarm(urldict,os.environ['mytopic'])
  
 datares={"Response" : msg, "httpMethod": events['httpMethod'], "body": events['body'] }
 return {'statusCode':200 , 'body':json.dumps(datares)}
############ The end