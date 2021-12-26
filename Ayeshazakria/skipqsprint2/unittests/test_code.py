import pytest
import aws_cdk as core
from skipqproject.pipeline_stack import PipelinesStack

# def test_code():
#     assert 2==2
    
    
def test_lambda():
   app=core.App()
   #creating stack named Stack
   PipelinesStack(app,"Stack")
   template=app.synth().get_stack_by_name("Stack").template
   functions=[ resource for resource in template["Resources"].values() if resource['Type']=='AWS::Lambda::Function']
   
   #Assert
   assert len(functions)==2