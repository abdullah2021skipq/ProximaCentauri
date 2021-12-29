from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam as aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db,
    aws_codedeploy as cdp
)
from resources import constants as constants
from resources.S3bucket import S3Bucket as sb
import json 
import random
import string
import datetime


class SprintTwoProjStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print("Sprint 2 Project stack instantiated :)")

        #####################################################################################################################
        ##                                 WebHealth Monitor Lambda Configuration                                          ##
        #####################################################################################################################
        
        lambda_role = self.create_lambda_role()
        WH_Lambda = self.create_lambda("SikandarS2WebHealthLambda", "./resources/", "WH_Lambda.lambda_handler", lambda_role,
                                        cdk.Duration.seconds(20))
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_targets = targets_.LambdaFunction(handler=WH_Lambda)
        rule = events_.Rule(self, "S2webHealth_Invocation", description="Periodic Lambda", enabled=True, schedule=lambda_schedule, targets=[lambda_targets])
        
        #####################################################################################################################
        ##                              Setting Up DynamoDB WebHealth Logging Table                                        ##
        #####################################################################################################################
        
        print("something again")
        db_table = self.create_db_table(id = "SprintTwoTable", part_key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        db_lambda_role = self.create_db_lambda_role()
        DB_Lambda = self.create_lambda("SikandarS2DBLambda", "./resources/", "DB_Lambda.lambda_handler", role=db_lambda_role)
        db_table.grant_full_access(DB_Lambda)
        DB_Lambda.add_environment('table_name', db_table.table_name)
        
        #####################################################################################################################
        ##                      Setting Up SNS Notifications for Email and Lambda Triggering                               ##
        #####################################################################################################################

        topic = sns.Topic(self, "S2webHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription(email_address = "sikandar.bakht.s@skipq.org"))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn = DB_Lambda))
        
        
        #####################################################################################################################
        ##                                 Retrieving Custom URLs from S3 Bucket                                           ##
        #####################################################################################################################
        
        URLS_MONITORED = sb('sikandarbakhtskipq').load('urls_dict.json')
        K=list(URLS_MONITORED['URLS'][0].keys())
        
        #####################################################################################################################
        ##                                      Creating Cloudwatch Metrics                                                ##
        #####################################################################################################################
        
        availability_metric = []
        latency_metric = []
        
        for i in range(len(K)):
            
            dimensions = {'URL': URLS_MONITORED['URLS'][0][K[i]]}
            availability_metric.append(
                                cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                                metric_name="S2"+constants.URL_MONITOR_NAME_AVAILABILITY,
                                dimensions_map = dimensions,
                                period = cdk.Duration.minutes(5),
                                label = f'{K[i]} Availability Metric')
                                )
                        
            latency_metric.append(
                                cloudwatch_.Metric(namespace = constants.URL_MONITOR_NAMESPACE,
                                metric_name="S2"+constants.URL_MONITOR_NAME_LATENCY,
                                dimensions_map = dimensions,
                                period = cdk.Duration.minutes(1),
                                label = f'{K[i]} Latency Metric')
                                )
      
        #####################################################################################################################
        ##                                        Creating Cloudwatch Alarms                                               ##
        #####################################################################################################################
        
        availability_alarm = []
        latency_alarm = []
        
        for i in range(len(K)):
            
            availability_alarm.append(
                                    cloudwatch_.Alarm(self, 
                                    id = f'Sikandar_Bakht_S2_{K[i]}_Availability_Alarm',
                                    alarm_description = f"Alarm to monitor availability of {K[i]}",
                                    metric = availability_metric[i],
                                    comparison_operator =cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                                    datapoints_to_alarm = 1,
                                    evaluation_periods = 1,
                                    threshold = 1)
                                    )
                                    
            latency_alarm.append(
                                    cloudwatch_.Alarm(self, 
                                    id = f'Sikandar_Bakht_S2_{K[i]}_Latency_Alarm',
                                    alarm_description = f"Alarm to monitor latency of {K[i]}",
                                    metric = latency_metric[i],
                                    comparison_operator =cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                    datapoints_to_alarm = 1,
                                    evaluation_periods = 1,
                                    threshold = constants.ALARM_THRESHOLDS[i])
                                )
        
        #####################################################################################################################
        ##                                        Adding Cloudwatch Alarms Actions                                         ##
        #####################################################################################################################
        
        for i in range(len(K)):
            
            availability_alarm[i].add_alarm_action(actions_.SnsAction(topic))
            latency_alarm[i].add_alarm_action(actions_.SnsAction(topic))
       
        #####################################################################################################################
        ##                                      Creating Rollback resources                                                ##
        #####################################################################################################################
        
        alias = lambda_.Alias(self, 
                             "S2WHLambdaAlias_"+construct_id,
                              alias_name="SikandarWHLambdaAlias_"+construct_id,
                              version=WH_Lambda.current_version)
                              
        rollback_alarm=cloudwatch_.Alarm(self, id="Sikandar_Rollback_Alarm",
                                        metric=WH_Lambda.metric_duration(period=cdk.Duration.minutes(1)),
                                        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                                        datapoints_to_alarm=1,
                                        evaluation_periods=1,
                                        threshold=8200) 
        
        rollback_alarm.add_alarm_action(actions_.SnsAction(topic))

        
                              
        cdp_role = self.create_codedeploy_role()

        cdp.LambdaDeploymentGroup(self, "WH_LambdaDeploymentGroup",
                                 alias=alias,
                                 deployment_config=cdp.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
                                 alarms=[rollback_alarm], role = cdp_role)
                                 
        #####################################################################################################################
        ##                                           Class Method Definitions                                              ##
        #####################################################################################################################
        
        
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
                        ])
            
        return lambdaRole
    
    def create_db_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                        ])
            
        return lambdaRole
        
    def create_codedeploy_role(self):
        lambdaRole = aws_iam.Role(self, "codedeploy_role",
                        assumed_by = aws_iam.ServicePrincipal('codedeploy.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambda_FullAccess')
                        ])
            
        return lambdaRole
        
    def create_lambda(self, id, asset, handler, role, timeout = cdk.Duration.seconds(3)):
        ### Creates a lambda function in python3.6
        return lambda_.Function(self, 
        id,
        handler=handler,  # optional, defaults to 'handler'
        runtime=lambda_.Runtime.PYTHON_3_6,
        code=lambda_.Code.from_asset(asset),
        role=role, timeout=timeout,
        description=str(datetime.datetime.now()) )
    
    def create_db_table(self, id, part_key):
        return db.Table(self, 
        id, 
        billing_mode=db.BillingMode.PAY_PER_REQUEST, 
        partition_key=part_key )
 