import boto3
############### to read all url from table ###### return list of url #######################################
class tablescan:
    def read_table(self,table_name):
        client = boto3.client('dynamodb')
        ####### get all data by scan function ########################################
        table_data = client.scan(TableName=table_name,AttributesToGet=['URL'])
        ######## extract url from data (array of dictionary ##########################
        url_list=table_data["Items"]
        ######### converting array of dictionary to array of string ##################
        for n in range(len(url_list)):
            url_list[n]=url_list[n]['URL']['S']
        # if no url in table  return message 
        if len(url_list)==0:
            return "Table has not Items(URL)"
        #if url are vaialble then return list of url
        return url_list


