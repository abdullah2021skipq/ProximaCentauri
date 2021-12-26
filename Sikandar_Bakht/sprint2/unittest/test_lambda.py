from aws_cdk import core as cdk
from sprint_two_proj.sprint_two_proj_stack import SprintTwoProjStack

def test_lambda():
    
    app = cdk.App()
    
    SprintTwoProjStack(app, "test_stack")
    template = app.synth().get_stack_by_name('test_stack').template
    function = [resource for resource in template['Resources'].values() if resource['Type'] == 'AWS::Lambda::Function']
    
    assert len(function)==2
    