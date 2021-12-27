import pytest
from aws_cdk import core 

from adeeldynamo_db.adeeldynamo_db_stack import  AdeeldynamoDbStack
def test_lambda():
    app = core.App()
    AdeeldynamoDbStack(app, 'Stack')
    temp = app.synth().get_stack_by_name('Stack').template
    lambda_function = [resource for resource in temp['Resources'].values() if resource['Type']=='AWS::IAM::Role']
    assert len(lambda_function)==2
    
