import pytest
from aws_cdk import core
#import aws_cdk.assertions as assertions
from sprint3_irfan.sprint3_irfan_stack import Sprint3IrfanStack
app=core.App()
Sprint3IrfanStack(app, 'Stack')
template=app.synth().get_stack_by_name('Stack').template
################# TEST 1: Lambda functions #############
def test_code():
    functions= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']
    assert 4==4