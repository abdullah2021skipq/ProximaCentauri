from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as event_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_
)
from constructs import Construct
from Resources import constants1 as constants

class AdeelWebAlarmStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role= self.create_lambda_role()
        # The code that defines your stack goes here
        WH_lamda = self.create_lambda('FirstHellammbda',"./Resources",'WAlambda.lambda_handler',lambda_role)
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = WH_lamda)
        our_rule = event_.Rule(self, id = "MonitorWebHealthMAtrix",enabled = True, schedule= lambda_schedule,targets = [lambda_target] )
        
        topic = sns.Topic(self,'WHtopic')
        topic.add_subscription(subscriptions_.EmailSubscription('adeel.shahzad.s@skipq.org'))
        
        dimension={'URL': constants.URL_TO_MONITOR}
        availability_matric=cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,metric_name = constants.URL_MONITOR_NAME_AVAILABILITY,dimensions_map=dimension,period=cdk.Duration.minutes(1))
        availability_alarm= cloudwatch_.Alarm(self,
        id = 'AvailabilityAlarm',
        metric = availability_matric,
        comparison_operator= cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods = 1,
        threshold = 1
        )


        latency_matric=cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,metric_name = constants.URL_MONITOR_NAME_LATENCY,dimensions_map=dimension,period=cdk.Duration.minutes(1))
        latency_alarm= cloudwatch_.Alarm(self,
        id = 'LatencyAlarm',
        metric = latency_matric,
        comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods = 1,
        threshold = 0.30
        )
        
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
        
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
