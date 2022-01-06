import pytest
from aws_cdk import core 

from adeel_project4.adeel_project4_stack import AdeelProject4Stack
app = core.App()
AdeelProject4Stack(app, 'Stack')
temp = app.synth().get_stack_by_name('Stack').template


################ testing number of lambda ############

def test_lambda():
    lambda_function = [resource for resource in temp['Resources'].values() if resource['Type']=='AWS::Lambda::Function']
    print(lambda_function)
    assert len(lambda_function)==5
    
################ testing number of IAMs ############
    
def test_iam():
    i_am_function = [resource for resource in temp['Resources'].values() if resource['Type']=='AWS::IAM::Role']
    assert len(i_am_function)==4
    
################ testing no of tables ############
    
def test_dynamo():
    dynamo_function = [resource for resource in temp['Resources'].values() if resource['Type']=='AWS::DynamoDB::Table']
    assert len(dynamo_function)==2
    
################ Testing buckets ############
    
def test_s3():
    s3_function = [resource for resource in temp['Resources'].values() if resource['Type']=='AWS::S3::Bucket']
    assert len(s3_function)==1
    
################ testing alarms ############
    
def test_alarm():
    alarm_function = [resource for resource in temp['Resources'].values() if resource['Type']=='AWS::CloudWatch::Alarm']
    assert len(alarm_function)==9