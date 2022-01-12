import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint3_irfan.sprint3_irfan_stack import Sprint3IrfanStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint2_irfan/sprint2_irfan_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint2IrfanStack(app, "sprint3_irfan")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
