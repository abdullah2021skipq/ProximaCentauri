import pytest
from aws_cdk import core
from pcwaheedproject2.pcwaheedproject2_stack import PcwaheedprojectStack
def test_lambda_stack():
    app = core.App()
    PcwaheedprojectStack(app,"waheedteststack")
    template=app.synth().get_stack_by_name('waheedteststack').template
    functions=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::Lambda::Function']
    assert len(functions)== 2

