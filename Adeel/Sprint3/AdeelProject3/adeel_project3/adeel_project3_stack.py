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
    aws_dynamodb as db,
    aws_codedeploy as codedeploy
)
from constructs import Construct
from resources1 import constants1 as constants
from resources1.bucket import Bucket as bo  

class AdeelProject3Stack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        ############################## Define lambda role and lambda functions###############################

        lambda_role= self.create_lambda_role()
        WH_lamda = self.create_lambda('FirstHellammbda',"./resources1/",'WH_ambda.lambda_handler',lambda_role)
        
        
         ############################## Schedule and Role functions for lambda ############################### 
         
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = WH_lamda)
        our_rule = event_.Rule(self, id = "MonitorWebHealthMAtrix",enabled = True, schedule= lambda_schedule,targets = [lambda_target] )
        
         ############################## Creating Dynamo table and giving it Premission ###############################
         
        dynamo_table=self.create_table(id='BDtable',
        key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        db_lambda_role = self.create_db_lambda_role()
        db_lamda = self.create_lambda('secondHellammbda',"./resources1/",'dynamo_lambda.lambda_handler',db_lambda_role)
        dynamo_table.grant_full_access(db_lamda)
        db_lamda.add_environment('table_name', dynamo_table.table_name)
        
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
        
         ##############################  Failure matrix creation ###############################
         
        duration_metric= cloudwatch_.Metric(namespace='AWS/Lambda', metric_name='Duration',
        dimensions_map={'FunctionName': WH_lamda.function_name}) 
        
        alarm_fail=cloudwatch_.Alarm(self, 'AlarmFail', metric=duration_metric, 
        threshold=10000, comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 
        evaluation_periods=1)
        ##Defining alias for my dblambda
        
        #versions = WH_lamda.add_version("new_version")
        WH_alias=self.create_alais(id = "AlaisForLambda",name = "AdeelLambdaVersion",
        version = WH_lamda.current_version)
        #### Defining code deployment group
        codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",alias=WH_alias,
        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
        alarms=[alarm_fail])
        
        
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
        timeout= cdk.Duration.minutes(10)
    )
    
     ################## Create table function ##############
     
    def create_table(self,id,key):
        return db.Table(self,id,
        partition_key=key)
        
    ################## Create alais function ##############    
        
    def create_alais(self,id,name,version):
        return lambda_.Alias(self , id , alias_name = name,
        version = version)