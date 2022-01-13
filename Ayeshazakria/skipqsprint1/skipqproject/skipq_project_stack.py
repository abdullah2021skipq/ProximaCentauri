from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_s3 as s3_,
    aws_dynamodb as db,
    
)

import boto3
#from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep


dynamodb_client = boto3.client('dynamodb')

from resources import constant as constants

class SkipqProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        lambda_role=self.create_lambda_role()

        Hwlambda=self.create_lambda("WebHealthLambda","./resources","webhealthlambda.lambda_handler",lambda_role)
        dynamodb_lambda=self.create_lambda("DynamoLambda","./resources","dynamo_lambda.lambda_handler",lambda_role)
        
        
        #Creating an event after every one minute
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
        
        #Setting target to our New  lambda for the event
        lambda_target= targets_.LambdaFunction(handler=Hwlambda)
        
        #defining rule for lambda function invokation event
        rule=events_.Rule(self, "WebHealth_Invokation",
            description="Periodic Lambda",enabled=True,
            schedule= lambda_schedule,
            targets=[lambda_target])
            
            
            
        # #creating s3 bucket
        
        # s3 = boto3.client('s3')
        # s3.create_bucket(Bucket='my-bucket')
        
        # filename = 'skipq_project_stack'
        # bucket_name = 'ayesha_bucket'
        
        # s3.upload_file(filename, bucket_name, filename)

            
        # #create table in dynamodb
        try:
            dynamo_db = self.create_table("DynamoTable")
        except dynamodb_client.exceptions.ResourceInUseException:
            print("Table Already Exists")
        
        dynamo_db.grant_full_access(dynamodb_lambda)
        
        topic = sns.Topic(self,"WebHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription(email_address="ayesha.zakria.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=dynamodb_lambda))
        

        dimension= {'URL': constants.URL_TO_MONITOR} #  cdk takes like this
        
        #create cloudwatch metric for availability
        availability_metric=cloudwatch_.Metric(
            namespace= constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
            dimensions_map=dimension, 
            period=cdk.Duration.minutes(1), 
            label='AvailabilityMetric'
            )
        
        #setting an alarm for availability
        availability_alarm= cloudwatch_.Alarm(self,
            id='Availability_alarm', 
            metric=availability_metric,
            comparison_operator= cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods=1,
            threshold= 1
            )
        
        dimension= {'URL': constants.URL_TO_MONITOR}
        
        #create a metric class for latency
        latency_metric=cloudwatch_.Metric(
            namespace= constants.URL_MONITOR_NAMESPACE, 
            metric_name=constants.URL_MONITOR_NAME_LATENCY,
            dimensions_map=dimension, 
            period=cdk.Duration.minutes(1),
            label='LatencyMetric'
            )
        
        #create an alarm for latency
        latency_alarm= cloudwatch_.Alarm(self,
            id='Latency_alarm', 
            metric=latency_metric,
            comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods=1,  
            threshold=0.30
            )
            
        #link sns and sns subscription to alarm
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))

    def create_lambda_role(self):
        lambdaRole=aws_iam.Role(self,"lambda-role",
        assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambdaInvocation-DynamoDB')
            ])
        return lambdaRole##

    def create_lambda(self,id,asset,handler, role):#
        return _lambda.Function(self, id,
        code=_lambda.Code.from_asset(asset),
        handler=handler,
        runtime=_lambda.Runtime.PYTHON_3_6,
        role=role
        )

    def create_table(self,id):
        dynamo_table = db.Table(
            self, 
            id,
            partition_key = db.Attribute(name="id", type=db.AttributeType.STRING),
            sort_key = db.Attribute(name="timestamp",type=db.AttributeType.STRING),
        )
        return dynamo_table













