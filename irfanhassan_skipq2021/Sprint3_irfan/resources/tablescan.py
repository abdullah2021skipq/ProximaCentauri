import boto3

class tablescan:
    def read_table(self,table_name):
        client = boto3.client('dynamodb')
        table_data = client.scan(TableName=table_name,AttributesToGet=['URL'])
        url_list=table_data["Items"]
        for n in range(len(url_list)):
            url_list[n]=url_list[n]['URL']['S']
        if len(url_list)==0:
            return "Table has not Items(URL)"
        return url_list


