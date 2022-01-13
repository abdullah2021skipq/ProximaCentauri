import pytest
from aws_cdk import core

from sprint2_irfan.sprint2_irfan_stack import Sprint2IrfanStack
def test_dynamodb():
    app = core.App()
    Sprint2IrfanStack(app, 'Stack')
    temp = app.synth().get_stack_by_name('Stack').template
    dynamodb_table = [resource for resource in temp['Resources'].values()  if resource['Type']=="AWS::DynamoDB::Table"]
    print(len(dynamodb_table))
    assert len(dynamodb_table)==1  #
    