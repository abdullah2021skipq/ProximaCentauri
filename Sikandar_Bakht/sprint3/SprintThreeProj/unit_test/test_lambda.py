import pytest
from aws_cdk import core
from sprint_three_proj.sprint_three_proj_stack import SprintThreeProjStack


app = core.App()
SprintThreeProjStack(app,"teststack")
template=app.synth().get_stack_by_name('teststack').template

def test_lambda_stack():
    functions=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::Lambda::Function']
    assert len(functions)==3
    
def test_sns():
    subs=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::SNS::Subscription']
    assert len(subs)==2
    
def test_table():
    tables=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::DynamoDB::Table']
    assert len(tables)==2
    
def test_S3_bucket():
    buckets=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::S3::Bucket']
    assert len(buckets)==1

def test_cloudwatch_alarms():
    alarms=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::CloudWatch::Alarm']
    assert len(alarms)==9
