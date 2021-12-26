import pytest
from aws_cdk import core
from skipqproject.sprint2_project_stack import SprintTwoProjectStack
def test_lambda():
    app=core.App()
    stack=SprintTwoProjectStack(app, 'sprint2stack')
    #template = assertions.Template.from_stack(stack)
    template=app.synth().get_stack_by_name('sprint2stack').template
    functions= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']
    assert len(functions)==2