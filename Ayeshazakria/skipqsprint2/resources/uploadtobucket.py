import boto3

def upload_file():
    # creating s3 bucket to upload urls.txt
    s3 = boto3.client('s3')
    try:
        s3.create_bucket(Bucket="ayeshaskipqbucket",CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2'})
        s3.upload_file("urls.txt", "ayeshaskipqbucket" ,"urls_list.txt")
    except:
        s3.upload_file("urls.txt", "ayeshaskipqbucket" ,"urls_list.txt")
        

def get_file(bucket, item):
    # function to read data from urls_list.txt
    name_url = []
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, item)
    for line in obj.get()['Body']._raw_stream.readline(): 
        name_url.append(line)
    return name_url

upload_file()