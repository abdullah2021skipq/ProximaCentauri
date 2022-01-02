import pytest
from aws_cdk import core
from sprint_three_proj.sprint_three_proj_stack import SprintThreeProjStack

def test_lambda_stack():
    app = core.App()
    SprintThreeProjStack(app,"teststack")
    
    template=app.synth().get_stack_by_name('teststack').template
    functions=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::Lambda::Function']
    assert len(functions)==3