import pytest
from aws_cdk import core

from sprint2_irfan.sprint2_irfan_stack import Sprint2IrfanStack
def test_code():
    app = core.App()
    Sprint2IrfanStack(app, 'Stack')
    temp = app.synth().get_stack_by_name('Stack').template
    lambda_function = [resource for resource in temp['Resources'].values()  if resource['Type']=="AWS::Lambda::Function"]
    assert len(lambda_function)==2
    
