from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as event_,
    aws_events_targets as targets_,
    aws_cloudwatch as cloudwatch_,
    aws_iam,
    aws_sns as sns,
    aws_sns_subscriptions as subsribe,
    aws_cloudwatch_actions as cw_actions,
    aws_dynamodb as db
)
#from aws_cdk import aws_cloudwatch_actions as actions_
from resources import constants as constant_
from resources.s3bucket_read import s3bucket_read as bucket 

class IrfanSkipQProject1Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        

        #creating lambda 
        lambda_role = self.create_lambda_role()
    #    hi_lamda = self.create_lambda('heloHellammbda',"./resources",'lambda.lambda_handler',lambda_role)
        hello_lamda = self.create_lambda('FirstHellammbda',"./resources",'Monitor_webhealth.lambda_handler',lambda_role)
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = hello_lamda)
        our_rule = event_.Rule(self, id = "MonitorwebHealth",enabled = True, schedule= lambda_schedule,targets =[lambda_target])
                
        #creating dynamodb table 
        dynamo_table=self.create_table(id='irfanhassantable',name = constant_.table_name, key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        db_lambda_role = self.create_db_lambda_role()
        db_lamda = self.create_lambda('secondHellammbda',"./resources/",'dynamodb_lambda.lambda_handler',db_lambda_role)
        dynamo_table.grant_full_access(db_lamda)
        
        
        
        #adding SNS 
        sns_topic = sns.Topic(self, 'WebHealth')
        sns_topic.add_subscription(subsribe.LambdaSubscription(fn = db_lamda))
        sns_topic.add_subscription(subsribe.EmailSubscription("muhammad.irfan.hassan.s@skipq.org"))
        
        
        list_url=bucket().bucket_as_list()
        #creating metrics for latency and availability
        for index in range (0,4):                    
        #creating alarm for avialability and latency  
            Dimensions={'URL': list_url[index]}
            availabilty_metric=cloudwatch_.Metric(namespace=constant_.URL_NameSpace, 
                    metric_name=constant_.URL_Aailibilty, 
                    dimensions_map=Dimensions,
                    period=cdk.Duration.minutes(1),
                    label=('availabilty_metric'+' '+list_url[index])
                    )
            availabilty_Alarm=cloudwatch_.Alarm(self, 
                    id ="AvailabiltyAlarm"+" "+list_url[index],
                    metric = availabilty_metric,
                    comparison_operator = cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                    datapoints_to_alarm=1,
                    evaluation_periods=1,
                    threshold =1
                    )

            latency_metric=cloudwatch_.Metric(namespace=constant_.URL_NameSpace, 
                    metric_name=constant_.URL_Latency, 
                    dimensions_map=Dimensions,
                    period=cdk.Duration.minutes(1),
                    label='latency_metric'+" "+list_url[index]
                    )
                    
          

            latency_Alarm=cloudwatch_.Alarm(self, id="latencyAlarm"+" "+list_url[index],
                    metric = latency_metric,
                    comparison_operator = cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                    datapoints_to_alarm=1,
                    evaluation_periods=1,
                    threshold = constant_.threshold[index]
                    )
        
        
        #sending sns topic to subscriber when alarm preached
            availabilty_Alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))
            latency_Alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))




#creating lambda role function to give all access to lambda
    def create_lambda_role(self):
        lambda_role = aws_iam.Role(self, "lambda-role", 
        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies = [
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSlambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess')
            ]
        )
        return lambda_role
  
        
#creating lambda handler    
    def create_lambda(self,id, asset, handler,role):
        return lambda_.Function(self, id,
        code = lambda_.Code.from_asset(asset),
        handler=handler,
        runtime= lambda_.Runtime.PYTHON_3_6,
        role=role
        )
        
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
#creating dynamo table 
    def create_table(self,id,name,key):
        return db.Table(self,id,
        table_name = name,
        partition_key=key)
    