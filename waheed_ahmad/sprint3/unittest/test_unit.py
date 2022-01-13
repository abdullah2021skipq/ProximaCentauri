import pytest
from aws_cdk import core
from sprint3.sprint3_stack import waheedsprint2
def test_lambda_stack():
    app = core.App()
    waheedsprint2(app,"waheedteststack")
    template=app.synth().get_stack_by_name('waheedteststack').template
    functions=[resource for resource in template['Resources'].values() if resource['Type']== 'AWS::Lambda::Function']
    assert len(functions)== 2

