import pytest
from aws_cdk import core
#import aws_cdk.assertions as assertions
from talha_project.talha_project_stack import TalhaProjectStack
app=core.App()
stack=TalhaProjectStack(app, 'infStack')
template=app.synth().get_stack_by_name('infStack').template
def test_lambda():
    #app=core.App()
    #stack=TalhaProjectStack(app, 'infStack')
    #template = assertions.Template.from_stack(stack)
  #  template=app.synth().get_stack_by_name('infStack').template
    functions= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']
    assert len(functions)>=4
def test_alarms():

    #template = assertions.Template.from_stack(stack)
    
    functions= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::CloudWatch::Alarm']
    assert len(functions)>3
    #8for metrics and  for failure alarm=9total
    
#Make sure that we have a bucket(necessary condition)
def test_bucket():
    #app=core.App()
    #stack=TalhaProjectStack(app, 'infStack')
    #template = assertions.Template.from_stack(stack)
    #template=app.synth().get_stack_by_name('infStack').template
    buckets= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::S3::Bucket']
    assert len(buckets)>=1
    
    #Make sure that we have a Table in which we will store the URLs
def test_table():
 #   app=core.App()
#    stack=TalhaProjectStack(app, 'infStack')
    #template = assertions.Template.from_stack(stack)
 #   template=app.synth().get_stack_by_name('infStack').template
    tables= [resource for resource in template['Resources'].values() if resource['Type']=='AWS::DynamoDB::Table']
    assert len(tables)>=1
    
    