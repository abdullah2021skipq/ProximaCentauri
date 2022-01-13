
from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda,
    aws_events as events_,
    aws_events_targets as targets_,# aws_sqs as sqs,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_s3 as s3_, 
    aws_dynamodb as db_,
  #  aws_lambda_event_sources as lambda_events_,
    aws_codedeploy as codedeploy
)
#import boto3
from resources import constants as constants
from resources import s3bucket_url 
#from resources import s3bucket_url.URLS as s3urls 

class TalhaProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role=self.create_lambda_role()
    # The code that defines your stack goes here
        HWlambda=self.create_lambda('FirstHWlambda', './resources','webHealth_talha_lambda.lambda_handler' ,lambda_role)
    #create table in dynamo db
        try:
            dynamo_table= self.create_table()
        except: pass
        #give read write permissions to our lambda
        tablekaname=dynamo_table.table_name
        constants.write_T(tablekaname)
        
        db_lambda_role = self.create_db_lambda_role()
        Talha_db_lambda=self.create_dblambda('neTwlambda', './resources','talha_dynamoDb_lambda.lambda_handler' ,db_lambda_role, environment={'table_name':tablekaname})
        dynamo_table.grant_read_write_data(Talha_db_lambda) 
    #Creating an event after every one minute
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
    #Setting target to our New WH lambda for the event##
        lambda_target= targets_.LambdaFunction(handler=HWlambda)
    #defining rule for lambda function invokation event
        rule=events_.Rule(self, "WebHealth_Invokation",
            description="Periodic Lambda",enabled=True,
            schedule= lambda_schedule,
            targets=[lambda_target])
         
        ###defining SNS service    
        topic = sns.Topic(self, "TalhaSkipQWebHealthTopic")
        #sns subscription with email
        topic.add_subscription( subscriptions_.EmailSubscription('talha.naeem.s@skipq.org'))
###Add lambda subscription to db_lambda, whenever an event occurs at the specified topic
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=Talha_db_lambda))
        listofurls=s3bucket_url.read_url_list()
        self.create_alarm(topic,listofurls)
        ############Creating Alarm on aws metrics for lambda function duration ###########
        metricduration= cloudwatch_.Metric(namespace='AWS/Lambda', metric_name='Duration',
            dimensions_map={'FunctionName': Talha_db_lambda.function_name}  )
        failure_alarm=cloudwatch_.Alarm(self, 'FailureAlarm', metric=metricduration,
            threshold=650,
            comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            evaluation_periods=1) 
                
        ##Defining alias for my lambda    
        #try:
        db_alias=_lambda.Alias(self, "TalhasAlias"+construct_id,
            alias_name="TalhasLaliass",
            version=Talha_db_lambda.current_version)
        #except: pass
        #### Defining code deployment group to auto roll back, on the basis of
        ####  aws lambda function's Alarm on metrics(Duration).               ########### 
        codedeploy.LambdaDeploymentGroup(self, "Talhaid",alias=db_alias,
             alarms=[failure_alarm])
 # Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        


    def create_lambda_role(self):
        lambdaRole=aws_iam.Role(self,"lambda-role",
        assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess')
            ]) 
        return lambdaRole##
    
    def create_db_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                        ])
            
        return lambdaRole

    def create_lambda( self,id,asset,handler, role):#
        return _lambda.Function(self, id,
        code=_lambda.Code.from_asset(asset),
        handler=handler,
        runtime=_lambda.Runtime.PYTHON_3_6,
        role=role,timeout= cdk.Duration.minutes(5)
        )
    def create_dblambda( self,id,asset,handler, role, environment):#
        return _lambda.Function(self, id,
        code=_lambda.Code.from_asset(asset),
        handler=handler,
        runtime=_lambda.Runtime.PYTHON_3_6,
        role=role,timeout= cdk.Duration.minutes(5),
        environment=environment
        )
        # example resource
        # queue = sqs.Queue(
        #     self, "TalhaProjectQueue",
        #     visibility_timeout=cdk.Duration.seconds(300),
        # )
    def create_table( self):#, table_name=constants.TABLE_NAME put back
        return db_.Table(self,id="Table" ,partition_key=db_.Attribute(name="id", type=db_.AttributeType.STRING), 
            sort_key=db_.Attribute(name="createdDate", type=db_.AttributeType.STRING))
####################################################################################################################
##      Generating Metrics and then raising alarms on them.                                                    ####
####################################################################################################################
    def create_alarm(self, topic, URLLS):
        for web in URLLS:
            dimension= {'URL':  web}
    #create cloudwatch metric for availability 
            availability_metric=(cloudwatch_.Metric( namespace=constants.URL_MONITOR_NAMESPACE,metric_name=web+constants.URL_MONITOR_NAME1A,
            dimensions_map=dimension, period=cdk.Duration.minutes(1), label=web+'Avaiability_metric'))
    #setting an alarm for availability
            availability_alarm=( cloudwatch_.Alarm(self,
                id=web+'Availability_alarm', metric=availability_metric,
                comparison_operator= cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD, 
                datapoints_to_alarm=1,
                evaluation_periods=1, 
                threshold= constants.THRESHOLD_AVAIL
                ))
    #create a metric class for latency
            latency_metric=(cloudwatch_.Metric(namespace= constants.URL_MONITOR_NAMESPACE, metric_name=web+constants.URL_MONITOR_NAME1L, 
                dimensions_map=dimension, period=cdk.Duration.minutes(1),label=web+'Latency_metric'))
    #create an alarm for latency
            latency_alarm=(cloudwatch_.Alarm(self,
                id=web+'Latency_alarm', metric=latency_metric,
                comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                datapoints_to_alarm=1,
                evaluation_periods=1,  
                threshold=constants.THRESHOLD_LATENCY
                ))
    #link sns and sns subscription to alarm
            availability_alarm.add_alarm_action(actions_.SnsAction(topic))
            latency_alarm.add_alarm_action(actions_.SnsAction(topic))
            
        