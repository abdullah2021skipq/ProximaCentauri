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
    aws_dynamodb as db,
    aws_codedeploy as codedeploy
)
#from aws_cdk import aws_cloudwatch_actions as actions_
from resources import constants as constant_

class Sprint3IrfanStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

########## #creating lambda roll and lambda for webhealth  ####################################################################

        lambda_role = self.create_lambda_role()
    #    hi_lamda = self.create_lambda('heloHellammbda',"./resources",'lambda.lambda_handler',lambda_role)
        webhealth_lambda = self.create_lambda('FirstHellammbda',"./resources",'Monitor_webhealth.lambda_handler',lambda_role)
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = webhealth_lambda)
        our_rule = event_.Rule(self, id = "MonitorwebHealth",enabled = True, schedule= lambda_schedule,targets =[lambda_target])
                
############ #creating dynamodb table to store alarm #############################################################

        dynamo_table=self.create_table(id='irfanhassantable', key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        db_lambda_role = self.create_db_lambda_role()
        db_lamda = self.create_lambda('secondHellammbda',"./resources/",'dynamodb_lambda.lambda_handler',db_lambda_role)
        dynamo_table.grant_full_access(db_lamda)

        db_lamda.add_environment('table_name', dynamo_table.table_name)
        
                
############ #creating dynamodb table to store url #############################################################
        s3bucket_lambda = self.create_lambda('s3bucketlammbda',"./resources",'s3_dynamodb.lambda_handler',lambda_role)
       
        url_table=self.create_table(id='urltable', key=db.Attribute(name="URL", type=db.AttributeType.STRING))
        url_table.grant_full_access(s3bucket_lambda)
        s3bucket_lambda.add_environment('urltable_name', url_table.table_name)
        
############# #adding SNS topic and adding dynao db lambda and myself as subscribe to sns topic using my email address #############
        
    #    sns_topic = sns.Topic(self, 'WebHealth')
    #    sns_topic.add_subscription(subsribe.LambdaSubscription(fn = db_lamda))
    #    sns_topic.add_subscription(subsribe.EmailSubscription("muhammad.irfan.hassan.s@skipq.org"))
        
##############  reading URL from json file in s3 bucket ##############################################        

      #  list_url=bucket().bucket_as_list();

#############  adding metrics and alarm for each webpage ##############################################

   #     for url in list_url:                   
   #         Dimensions={'URL': url }
            
        ############# adding availability matrics into cloud watch #################################
        
    #        availabilty_metric=cloudwatch_.Metric(namespace=constant_.URL_NameSpace, 
    #                metric_name=constant_.URL_Aailibilty, 
    #                dimensions_map=Dimensions,
    #                period=cdk.Duration.minutes(0.5),
   #                 label=('availabilty_metric'+' '+url )
   #                 )
                    
        ############# adding availability AlARM on availabilty metric into cloud watch #################################
  #          availabilty_Alarm=cloudwatch_.Alarm(self, 
  #                  id ="AvailabiltyAlarm"+" "+url ,
  #                  metric = availabilty_metric,
  #                  comparison_operator = cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
  #                  datapoints_to_alarm=1,
   #                 evaluation_periods=1,
   #                 threshold =1
   #                 )
        ############# adding latency matrics into cloud watch #################################
   #         latency_metric=cloudwatch_.Metric(namespace=constant_.URL_NameSpace, 
  #                  metric_name=constant_.URL_Latency, 
  #                  dimensions_map=Dimensions,
 #                   period=cdk.Duration.minutes(0.5),
#                    label='latency_metric'+" "+url 
  #                  )
               #     
        ############# adding  AlARM on latency metric into cloud watch #################################            
   #         latency_Alarm=cloudwatch_.Alarm(self, id="latencyAlarm"+" "+url ,
   #                 metric = latency_metric,
   #                 comparison_operator = cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
    #                datapoints_to_alarm=1,
   #                 evaluation_periods=1,
   #                 threshold = .28
   #                 )
        #
        ######### #sending sns topic to subscriber when alarm preached ##############################
  #          availabilty_Alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))
 #          latency_Alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))
            
#############    Automate ROLBACNK  ############################################################

  #      durationMetric= cloudwatch_.Metric(namespace='AWS/Lambda', metric_name='Duration',
  #      dimensions_map={'FunctionName': webhealth_lambda.function_name},period=cdk.Duration.minutes(1)) 
        #if it failed then alarm generate.. 
   #     alarm_indication_Failed=cloudwatch_.Alarm(self, 'Alarm_indication_Failed', metric=durationMetric, 
   #     threshold=5000, comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 
  #      evaluation_periods=1)
        ###Defining alias of  my web health lambda 
   #     Web_health_alias=lambda_.Alias(self, "AlaisForWebHealthLambda", alias_name="Web_Health_Alias",
    #    version=webhealth_lambda.current_version) 
        #### Defining code deployment when alarm generate .
   #     codedeploy.LambdaDeploymentGroup(self, "id",alias=Web_health_alias, alarms=[alarm_indication_Failed])


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
    #### adding policy for dynamo db lambda to give it fullaccess
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
    def create_table(self,id,key):
        return db.Table(self,id,
        partition_key=key)
        #finish