import aws_cdk as core
import aws_cdk.assertions as assertions

from testenv.testenv_stack import TestenvStack

# example tests. To run these tests, uncomment this file along with the example
# resource in testenv/testenv_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TestenvStack(app, "testenv")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
