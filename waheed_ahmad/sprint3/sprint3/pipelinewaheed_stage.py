from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as event_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db
)
from aws_cdk import core
from sprint3.sprint3_stack import waheedsprint2

class ProductionStage(core.Stage):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        waheed_db_stack2=waheedsprint2(self,"waheedstack2")  #stage for adding stage