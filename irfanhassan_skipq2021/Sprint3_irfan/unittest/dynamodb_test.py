import pytest
from aws_cdk import core
#import aws_cdk.assertions as assertions
from sprint3_irfan.sprint3_irfan_stack import Sprint3IrfanStack
app=core.App()
Sprint3IrfanStack(app, 'Stack')
template=app.synth().get_stack_by_name('Stack').template
#unit test to check number of dynamo DB table 
def test_dynamodb():
    dynamodb_table = [resource for resource in template['Resources'].values()  if resource['Type']=="AWS::DynamoDB::Table"]
    assert len(dynamodb_table)>=2
    #assert 2==2  #
    #
    


    
    