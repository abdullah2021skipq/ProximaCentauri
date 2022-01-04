from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db,
    aws_codedeploy as codedeploy,
    aws_apigateway as gateway
)
from resources import constants as constants
from resources import s3bucket
from resources import sprint3_dynamo
import os

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class PcRepoAzbStack1(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # s3 bucket
        s3bucket.store_file("abdullahzamanbucket")
        URL_list = s3bucket.read_file("abdullahzamanbucket", "urlsList.json")
        print(URL_list)

        
        # The code that defines your stack goes here
        lambda_role = self.create_lambda_role()
        hw_lambda = self.create_lambda("FirstHWLambda", "./resources", "webhealth_lambda.lambda_handler", lambda_role)
        db_lambda = self.create_lambda("DynamoLambda", "./resources", "dynamodb_lambda.lambda_handler", lambda_role)
        
        #******************** SPRINT 3 DYNAMO TABLE ****************************
        sprint3_dynamo.create_sprint3_table()
        sprint3_dynamo.putting_sprint3_data()
        sprint3_lambda = self.create_lambda("sprint3Lambda", "./resources", "sprintt3_lambda.lambda_handler", lambda_role)
        # Making an api gateway
        api = self.create_gateway('AzbApi',sprint3_lambda)
        api_resource1 = api.root.add_resource("health")
        api_resource1.add_method("GET") # GET /health
        api_resource2 = api.root.add_resource("url")
        api_resource2.add_method("GET")
        api_resource2.add_method("POST")
        api_resource2.add_method("DELETE")
        api_resource2.add_method("PATCH")
        api_resource3 = api.root.add_resource("urls")
        api_resource3.add_method("GET")
        
        # We define the schedule, target and the rule for our lambda
        
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler=hw_lambda)
        rule = events_.Rule(self, "WebHealth_Invocation", description = "Periodic Lambda",      # rule: which targets will get our event
                            enabled=True, schedule=lambda_schedule, targets=[lambda_target])
        
        dynamo_table = self.create_table(os.getenv('table_name'), "AlarmDetails")
        dynamo_table.grant_read_write_data(db_lambda)
        db_lambda.add_environment('table_name',dynamo_table.table_name)
        
        topic = sns.Topic(self, "WebHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription("abdullah.zaman.babar.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=db_lambda))
        
        
        
        dimension = {"URL" : constants.URL_TO_MONITOR}
        availability_metric = cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,
                                            metric_name=constants.URL_MONITOR_NAME_Availability, 
                                            dimensions_map=dimension, 
                                            period=cdk.Duration.minutes(1), label="Availability Metric")
        availability_alarm = cloudwatch_.Alarm(self, id="AvailabilityAlarm",
                                        metric=availability_metric,
                                        comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                                        datapoints_to_alarm=1,
                                        evaluation_periods=1,
                                        threshold=1)
                                        
        dimension = {"URL" : constants.URL_TO_MONITOR}
        latency_metric = cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,
                                            metric_name=constants.URL_MONITOR_NAME_Latency, 
                                            dimensions_map=dimension, 
                                            period=cdk.Duration.minutes(1), label="Latency Metric")
        latency_alarm = cloudwatch_.Alarm(self, id="LatencyAlarm",
                                        metric=latency_metric,
                                        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                        datapoints_to_alarm=1,
                                        evaluation_periods=1,
                                        threshold=0.28)
    
        # ROLLBACK to the previous version if an alarm is raised
        metric_roll = cloudwatch_.Metric(namespace='AWS/Lambda', metric_name='Duration',
                                        dimensions_map={'FunctionName':hw_lambda.function_name},
                                        period= cdk.Duration.minutes(1))
    
        alarm_roll = cloudwatch_.Alarm(self, id="RollBackAlarm", metric= metric_roll,
                                        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                        datapoints_to_alarm=1,
                                        evaluation_periods=1,
                                        threshold=2000)         # 3000 ms = 3 sec
        
        alarm_roll.add_alarm_action(actions_.SnsAction(topic))
       
        alias = lambda_.Alias(self, "LambdaAlias",alias_name="Lambda",version=hw_lambda.current_version)
        
        codedeploy.LambdaDeploymentGroup(self, "WebHealth Lambda", alias=alias,
                                        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
                                        alarms=[alarm_roll]
        )
        
        
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
        

    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
             assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('IAMFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaInvocation-DynamoDB"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayAdministrator"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayPushToCloudWatchLogs"),
                #aws_iam.ManagedPolicy.from_aws_managed_policy_name("APIGatewayServiceRolePolicy"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
                
                ])
        return lambdaRole

    def create_table(self, t_name, par_key):
        try:
            return db.Table(self, id="Table", table_name=t_name,
                        partition_key=db.Attribute(name=par_key, type=db.AttributeType.STRING))
        except:
            pass
    
    def create_lambda(self, newid, asset, handler, role):
        return lambda_.Function(self, id = newid,
                                runtime = lambda_.Runtime.PYTHON_3_6,
                                handler = handler,
                                code = lambda_.Code.asset(asset),
                                role=role,
    			                    )
    
    def create_gateway(self, name, handler):
        return gateway.LambdaRestApi(self, id=name, handler=handler,
                                    proxy=False
        )
    			         
