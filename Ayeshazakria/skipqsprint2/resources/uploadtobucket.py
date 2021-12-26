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
        