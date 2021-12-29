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
    aws_codedeploy as codedeploy
)
import boto3

dynamodb_client = boto3.client('dynamodb')
import skipqproject.constant as constants

class SprintTwoProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role=self.create_lambda_role()
        # The code that defines your stack goes here
        HWlambda=self.create_lambda('WebHealthLambda', './resources','webhealthlambda.lambda_handler' ,lambda_role)
        
        dynamodb_lambda=self.create_lambda('Dynamolambda', './resources','dynamo_lambda.lambda_handler' , lambda_role)
 
        #Creating an event after every one minute
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
        #Setting target to our New WH lambda for the event##
        lambda_target= targets_.LambdaFunction(handler=HWlambda)
        #defining rule for lambda function invokation event
        rule=events_.Rule(self, "WebHealth_Invokation",
            description="Periodic Lambda",enabled=True,
            schedule= lambda_schedule,
            targets=[lambda_target])
            
            
        #create table in dynamo db
        try:
            dynamo_db = self.create_table("DynamoTable")
        except dynamodb_client.exceptions.ResourceInUseException:
            print("Table Already Exists")
        
        dynamo_db.grant_full_access(dynamodb_lambda)
        dynamodb_lambda.add_environment('table_name', dynamo_db.table_name)
        
        ###defining SNS service    
        topic = sns.Topic(self,"WebHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription(email_address="ayesha.zakria.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=dynamodb_lambda))

        # urls = self.get_file("ayeshaskipqbucket","urls_list.txt")
        # for url in urls:
        #     print(url)
        dimension= {'URL':constants.URL_TO_MONITOR}
        
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
        
        # sprint2 work starts here
        rollback_metric=cloudwatch_.Metric(
        namespace='AWS/Lambda',
        metric_name='Duration',
        dimensions_map={'FunctionName':HWlambda.function_name},
        period= cdk.Duration.minutes(1))
    
        rollback_alarm= cloudwatch_.Alarm(self,
        id="RollbackAlarm",
        metric= rollback_metric,
        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods=1,
        threshold=2) # THRESHOLD IS IN MILLISECONDS
        
        rollback_alarm.add_alarm_action(actions_.SnsAction(topic))

        alias = _lambda.Alias(self, "WebHealthLambdaAlias"+construct_id,alias_name="Lambda",version=HWlambda.current_version)

        codedeploy.LambdaDeploymentGroup(self, "AyeshaWebHealthLambda_DeploymentGroup",
        alias=alias,
        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
        alarms=[rollback_alarm]
        )


    def create_lambda_role(self):
        lambdaRole=aws_iam.Role(self,"lambda-role",
        assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambdaInvocation-DynamoDB')
            ])
        return lambdaRole

    
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
    
    
    def get_file(self,bucket, item):
    # function to read data from urls_list.txt
        
        name_url = []
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, item)
        for line in obj.get()['Body']._raw_stream.readline(): 
            name_url.append(line)
        return name_url
