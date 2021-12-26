import pytest
from aws_cdk import core
from sprint_two_proj.sprint_two_proj_stack import SprintTwoProjStack

def test_lambda_stack():
    app = core.App()
    SprintTwoProjStack(app,"teststack")
    
    template=app.synth().get_stack_by_name('teststack').template
    functions=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::Lambda::Function']
    assert len(functions)== 2