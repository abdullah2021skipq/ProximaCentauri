from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_cloudwatch_actions as actions_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_codedeploy as codedeploy,
    aws_dynamodb as db
    #aws_s3 as s3,
    #aws_sqs as sqs,
    #aws_s3_notifications as s3n
)
#import Construct as Construct
from resources import constants as constants
import resources as resources
#from aws_cdk import core
URL_TO_MONITOR='www.twitter.com'
URL_MONITOR_NAMESPACE="waheedwebhealth"
URL_MONIROR_NAME_AVAILABILITY= "url_availability"
URL_MONIROR_NAME_LATENCY= "url_latency"


class PcwaheedprojectStack(cdk.Stack):

    
    
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)



###########defining roles
        lambda_role= self.create_lambda_role()
        hw_lambda = self.create_lambda('lambda', './resources', 'webhealthmonitor.lambda_handler', lambda_role)
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target=targets_.LambdaFunction(handler=hw_lambda)
        rule= events_.Rule(self, "webHealth_invoke", 
                            description= "call lambda periodic", 
                            enabled= True ,
                            schedule= lambda_schedule,
                            targets= [lambda_target]) #remeber the braces, i spent so much time to figure out this error, cz this is treateda as array
        
        
        ####### dynamoo table 
        dynamo_table=self.create_table(id='waheedalarmtable',
                                        key=db.Attribute(name="Timestamp",
                                        type=db.AttributeType.STRING))
        db_lambda_role = self.create_dbtable_lambda_role()
        db_lambda = self.create_lambda("DynamoDBLambda", "./resources", 'dynamodb_lambda.lambda_handler', lambda_role)
        
        dynamo_table.grant_full_access(db_lambda)
        db_lambda.add_environment('table_name', dynamo_table.table_name)
        
        # waheedbucket= s3.Bucket(self, "waheedbkt")
    
        # queue = sqs.Queue(self, 'buckQ',
        # visibility_timeout=cdk.Duration.seconds(300) ) 
        #waheedbucket.add_event_notification( s3.EventType.OBJECT_CREATED, s3n.SqsDestination(queue) )
        
        db.table.grant_read_write_data(db_lambda)
        #####also provide full read write access to table
        
        #####module code for sending sns notifications########################################################
        topic =sns.Topic(self, "webhealthmonitor")
        topic.add_subscription(subscriptions_.EmailSubscription('waheed.ahmad.s@skipq.org'))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=db_lambda))
        
        
        
        
        #for urls in s3_buckk
        dimension={'URL' :URL_TO_MONITOR}
       #####alarm to raise, sprint 2 pipeline
        duration_metric=cloudwatch_.Metric(namespace = 'AWS/Lambda', 
                                                metric_name = 'Duration',
                                                dimensions_map = {'FunctionName' : hw_lambda.function_name})
        failure_alarm= cloudwatch_.Alarm(self, 
			id='pipelinealarm',
			metric= duration_metric , 
			comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 
			evaluation_periods=1,
		 	threshold=350)   
        availability_metric=cloudwatch_.Metric(namespace=URL_MONITOR_NAMESPACE, 
                                                metric_name= URL_MONIROR_NAME_AVAILABILITY,
                                                dimensions_map=dimension,
                                                period=cdk.Duration.minutes(1),
                                                label= 'Availability Metric')
        availability_alarm= cloudwatch_.Alarm(self, 
			id='AvailabilityAlarm',
			metric= availability_metric , 
			comparison_operator= cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD  , 
			datapoints_to_alarm=1, 
			evaluation_periods=1,
		 	threshold=1)    
    
        dimension={'URL':URL_TO_MONITOR}
        latency_metric=cloudwatch_.Metric(namespace=URL_MONITOR_NAMESPACE, 
                                         metric_name=URL_MONIROR_NAME_LATENCY,
                                         dimensions_map=dimension,
                                         period=cdk.Duration.minutes(1),
                                         label= 'latency Metric' )
        latency_alarm= cloudwatch_.Alarm(self, 
			id='LatencyAlarm',
			metric= latency_metric , 
			comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD , 
			datapoints_to_alarm=1, 
			evaluation_periods=1,
		 	threshold=0.25 )
    
    ##########link the alarm to subscription
        
        
        myalias = lambda_.Alias(self, "LambdaAlias",
                            alias_name="waheedpipelinealias",
                            version= hw_lambda.current_version)

        codedeploy.LambdaDeploymentGroup(self, "webhealthmonitor",
                                        alias= myalias,
                                        alarms = [failure_alarm])
        
        
        # codedeploy.LambdaDeploymentConfig(self, 
        # "code" ,
        # alias,
        # LINEAR_10_PERCENT_EVERY_5_MINUTE,
        # alarms=[failure_alarm])
        # failure_alarm.add_alarm_action(actions_.SnsAction(topic))
        # availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        # latency_alarm.add_alarm_action(actions_.SnsAction(topic))
    
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
                        ])
        return lambdaRole
    def create_dbtable_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
                        ])
        return lambdaRole
        
    def create_alais(self,id,name,version):
        return lambda_.Alias(self , id , alias_name = name,
        version = version)
        
    def create_lambda(self, id, asset,handler, role):
        return lambda_.Function(self, id,
        runtime=lambda_.Runtime.PYTHON_3_6 ,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        role=role
)
     ### create table ###
     
    def create_table(self,id,key):
        return db.Table(self,id,
        partition_key=key)
        
        
   
