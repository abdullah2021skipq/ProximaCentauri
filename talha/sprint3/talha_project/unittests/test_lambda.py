import pytest
from aws_cdk import core
#import aws_cdk.assertions as assertions
from talha_project.talha_project_stack import TalhaProjectStack
app=core.App()
stack=TalhaProjectStack(app, 'infStack')
template=app.synth().get_stack_by_name('infStack').template
################# TEST 1: Lambda functions #############
def test_lambda():
    functions= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']
    assert len(functions)>=4
    
################# TEST 2: Alarms on metrics #############
def test_alarms():
    functions= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::CloudWatch::Alarm']
    assert len(functions)>3
    #8for metrics and  for failure alarm=9total

################# TEST 3: S3 bucket Test #############
#Make sure that we have a bucket(necessary condition)
def test_bucket():
    buckets= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::S3::Bucket']
    assert len(buckets)>=1
    
################# TEST 4: Dynamodb Tables #############
    #Make sure that we have a Table in which we will store the URLs
def test_table():
 
    tables= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::DynamoDB::Table']
    assert len(tables)>=1
    
# API invoke link: https://4jd8g9kea3.execute-api.us-east-2.amazonaws.com/prod/