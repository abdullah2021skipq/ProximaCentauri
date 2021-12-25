import pytest 
from aws_cdk import core
from pc_repo_azb.pc_repo_azb_stack import PcRepoAzbStack1


def lambda_test():
    
    app=core.App()
    PcRepoAzbStack1(app,'Stack')
    template=app.synth().get_stack_by_name('Stack').template
    fun=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']

    assert len(fun)==2