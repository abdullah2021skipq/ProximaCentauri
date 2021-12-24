##########################Importing All the nessearry libraries#######################################
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
from constructs import Construct
from resources1 import constants1 as constants
from resources1.bucket import Bucket as bo  

class AdeeldynamoDbStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        ############################## Define lambda role and lambda functions###############################

        lambda_role= self.create_lambda_role()
        WH_lamda = self.create_lambda('FirstHellammbda',"./resources1/",'WAMangoDBlambda.lambda_handler',lambda_role)
        
        
         ############################## Schedule and Role functions for lambda ############################### 
         
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = WH_lamda)
        our_rule = event_.Rule(self, id = "MonitorWebHealthMAtrix",enabled = True, schedule= lambda_schedule,targets = [lambda_target] )
        
         ############################## Creating Dynamo table and giving it Premission ###############################
        try:
            dynamo_table=self.create_table(id='BDtable',name = "AdeelAlarmdynamo",
            key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        except:
            pass
        db_lambda_role = self.create_db_lambda_role()
        db_lamda = self.create_lambda('secondHellammbda',"./resources1/",'dynamo_lambda.lambda_handler',db_lambda_role)
        dynamo_table.grant_full_access(db_lamda)
        
         ############################## Subscriptions ###############################
        
        topic = sns.Topic(self,'WHtopic')
        topic.add_subscription(subscriptions_.EmailSubscription('adeel.shahzad.s@skipq.org'))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=db_lamda)) 
        
         ############################## Alarms on cloud watch ###############################
        
        Url_Monitor = bo().bucket_as_list()
        b=1
        for url in Url_Monitor:
            
             ############################## Availability matrix and alarm for availability ###############################
            
            dimension={'URL': url}
            availability_matric=cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,metric_name = constants.URL_MONITOR_NAME_AVAILABILITY+'_'+url+str(b),dimensions_map=dimension,period=cdk.Duration.minutes(1))
            availability_alarm= cloudwatch_.Alarm(self,
            id = 'AvailabilityAlarm'+'_'+url,
            metric = availability_matric,
            comparison_operator= cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods = 1,
            threshold = 1
            )
            
            
             ############################## Latency Matrix and latency alarms ###############################


            latency_matric=cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,metric_name = constants.URL_MONITOR_NAME_LATENCY+'_'+url+str(b),dimensions_map=dimension,period=cdk.Duration.minutes(1))
            latency_alarm= cloudwatch_.Alarm(self,
            id = 'LatencyAlarm'+'_'+url,
            metric = latency_matric,
            comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods = 1,
            threshold = 0.28
            )
        
            availability_alarm.add_alarm_action(actions_.SnsAction(topic))
            latency_alarm.add_alarm_action(actions_.SnsAction(topic))
            b+=1
        
         ##############################  role for Cloud watch ###############################
        
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self,"lambda-role",
        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies = [aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"), 
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
        ])
        return lambdaRole
        
         ############################## role for dynamo ###############################
        
    def create_db_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
                        ])
        return lambdaRole
        
         ############################## Creating lambda and table creation function ###############################
        
        
    def create_lambda(self,id, asset, handler,role):
        return lambda_.Function(self, id,
        code = lambda_.Code.from_asset(asset),
        handler=handler,
        runtime= lambda_.Runtime.PYTHON_3_6,
        role=role,
        timeout= cdk.Duration.minutes(5)
    )
    def create_table(self,id,name,key):
        return db.Table(self,id,
        table_name = name,
        partition_key=key)