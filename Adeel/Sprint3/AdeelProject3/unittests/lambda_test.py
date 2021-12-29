import pytest
from aws_cdk import core 

from adeel_project3.adeel_project3_stack import AdeelProject3Stack
def test_lambda():
    app = core.App()
    AdeelProject3Stack(app, 'Stack')
    temp = app.synth().get_stack_by_name('Stack').template
    lambda_function = [resource for resource in temp['Resources'].values() if resource['Type']=='AWS::IAM::Role']
    assert len(lambda_function)==3
    
