import pytest
from aws_cdk import core
#import aws_cdk.assertions as assertions
from sprint4_irfan.sprint4_irfan_stack import Sprint4IrfanStack
app=core.App()
Sprint4IrfanStack(app, 'Stack')
template=app.synth().get_stack_by_name('Stack').template
#unit test to check number of s3bucket 
def test_s3bucket():
    s3bucket = [resource for resource in template['Resources'].values()  if resource['Type']=="AWS::S3::Bucket"]
    assert len(s3bucket)>=1
    
    #


    
    