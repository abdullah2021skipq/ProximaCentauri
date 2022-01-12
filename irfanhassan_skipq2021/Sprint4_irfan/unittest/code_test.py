import pytest
from aws_cdk import core
#import aws_cdk.assertions as assertions
from sprint4_irfan.sprint4_irfan_stack import Sprint4IrfanStack
app=core.App()
Sprint4IrfanStack(app, 'Stack')
template=app.synth().get_stack_by_name('Stack').template
################# TEST 1: Lambda functions #############
def test_code():
    functions= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']
    print(len(functions))
    assert len(functions)>=4
    #assert 4==4