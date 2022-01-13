import aws_cdk as core
import aws_cdk.assertions as assertions

from adeeldynamo_db.adeeldynamo_db_stack import AdeeldynamoDbStack

# example tests. To run these tests, uncomment this file along with the example
# resource in adeeldynamo_db/adeeldynamo_db_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AdeeldynamoDbStack(app, "adeeldynamo-db")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
