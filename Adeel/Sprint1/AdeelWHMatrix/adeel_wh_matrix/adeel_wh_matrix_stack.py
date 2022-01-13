from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as event_,
    aws_events_targets as targets_,
    aws_iam
)
from constructs import Construct

class AdeelWhMatrixStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role= self.create_lambda_role()
        # The code that defines your stack goes here
        WH_lamda = self.create_lambda('FirstHellammbda',"./resources",'WHMatrixlambda.lambda_handler',lambda_role)
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = WH_lamda)
        our_rule = event_.Rule(self, id = "MonitorWebHealthMAtrix",enabled = True, schedule= lambda_schedule,targets = [lambda_target] )
    
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self,"lambda-role",
        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies = [aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess')
        ])
        return lambdaRole
        
    def create_lambda(self,id, asset, handler,role):
        return lambda_.Function(self, id,
        code = lambda_.Code.from_asset(asset),
        handler=handler,
        runtime= lambda_.Runtime.PYTHON_3_6,
        role=role
        
    )