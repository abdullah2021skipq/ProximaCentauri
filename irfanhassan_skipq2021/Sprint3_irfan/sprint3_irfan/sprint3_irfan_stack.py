from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as event_,
    aws_events_targets as targets_,
    aws_cloudwatch as cloudwatch_,
    aws_iam,
    aws_lambda_event_sources as sources,
    aws_s3 as s3,
    aws_sns as sns,
    aws_sns_subscriptions as subsribe,
    aws_cloudwatch_actions as cw_actions,
    aws_dynamodb as db,
    aws_codedeploy as codedeploy,
    aws_apigateway as apigateway_
)
from resources import constants as constant_
from resources.s3bucket_read import s3bucket_read as bucket_ 

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
                
############ #creating dynamodb table  #############################################################

        dynamo_table=self.create_table(id='irfanhassantable', key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        db_lambda_role = self.create_db_lambda_role()
        db_lamda = self.create_lambda('secondHellammbda',"./resources/",'dynamodb_lambda.lambda_handler',db_lambda_role)
        dynamo_table.grant_full_access(db_lamda)

############## adding dynamo db table name in table_name variale ##################################
        db_lamda.add_environment('table_name', dynamo_table.table_name)
        
############# #adding SNS topic and adding dynao db lambda and myself as subscribe to sns topic using my email address #############
        
        sns_topic = sns.Topic(self, 'WebHealth')
        sns_topic.add_subscription(subsribe.LambdaSubscription(fn = db_lamda))
        sns_topic.add_subscription(subsribe.EmailSubscription("muhammad.irfan.hassan.s@skipq.org"))
    
############ #creating dynamo table to store URL  ###################################################################################
        url_lambda = self.create_lambda('urllammbda',"./resources",'s3_dynamodb_lambda.lambda_handler',db_lambda_role)
        url_table=self.create_table(id='irfanurltable', key=db.Attribute(name="URL", type=db.AttributeType.STRING))
        url_table.grant_full_access(url_lambda)
        url_lambda.add_environment('table_name', url_table.table_name)
        #table_name=url_table['"TableDescription']['TableName']
####    adding s3bucket event to trigger url_labda       ##########################################################################
        bucket = s3.Bucket(self, "urls3bucket")
        url_lambda.add_event_source(sources.S3EventSource(bucket,
                          events=[s3.EventType.OBJECT_CREATED],filters=[s3.NotificationKeyFilter(suffix=".json")]))

####### Adding API GateWay ##########################################################################################################
        apigateway_lambda=self.create_lambda('ApiGateWayLambda', './resources','apigateway_lambda.lambda_handler' ,db_lambda_role)
        apigateway_lambda.grant_invoke( aws_iam.ServicePrincipal("apigateway.amazonaws.com"))
        apigateway_lambda.add_environment('table_name', url_table.table_name)
        url_table.grant_full_access(apigateway_lambda)
        url_table.grant_full_access(webhealth_lambda)
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/README.html
        api = apigateway_.LambdaRestApi(self, "irfanAPI",handler=apigateway_lambda) #REST API
        
        items = api.root.add_resource("items")
        items.add_method("GET") # GET items
        items.add_method("PUT") # PUT items
        items.add_method("DELETE") # PUT items
        items.add_method("POST")  #update items
    
        
##############  reading URL from URL DynamoDB table  ##############################################        
        #
        list_url=bucket_(constant_.bucket,constant_.file_name).bucket_as_list();

#############  adding metrics and alarm for each webpage ##############################################

        for url in list_url:                   
            Dimensions={'URL': url }
            
        ############# adding availability matrics into cloud watch #################################
        
            availabilty_metric=cloudwatch_.Metric(namespace=constant_.URL_NameSpace, 
                    metric_name=constant_.URL_Aailibilty, 
                    dimensions_map=Dimensions,
                    period=cdk.Duration.minutes(0.5),
                    label=('availabilty_metric'+' '+url )
                    )
                    
        ############# adding availability AlARM on availabilty metric into cloud watch #################################
            availabilty_Alarm=cloudwatch_.Alarm(self, 
                    id ="AvailabiltyAlarm"+" "+url ,
                    metric = availabilty_metric,
                    comparison_operator = cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                    datapoints_to_alarm=1,
                    evaluation_periods=1,
                    threshold =1
                    )
        ############# adding latency matrics into cloud watch #################################
            latency_metric=cloudwatch_.Metric(namespace=constant_.URL_NameSpace, 
                    metric_name=constant_.URL_Latency, 
                    dimensions_map=Dimensions,
                    period=cdk.Duration.minutes(0.5),
                    label='latency_metric'+" "+url 
                    )
               #     
        ############# adding  AlARM on latency metric into cloud watch #################################            
            latency_Alarm=cloudwatch_.Alarm(self, id="latencyAlarm"+" "+url ,
                    metric = latency_metric,
                    comparison_operator = cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                    datapoints_to_alarm=1,
                    evaluation_periods=1,
                    threshold = 0.32
                    )
        #
        ######### #sending sns topic to subscriber when alarm preached ##############################
            availabilty_Alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))
            latency_Alarm.add_alarm_action(cw_actions.SnsAction(sns_topic))
            
#############    Automate ROLBACNK  ############################################################

        #durationMetric= cloudwatch_.Metric(namespace='AWS/Lambda', metric_name='Duration',
        #dimensions_map={'FunctionName': webhealth_lambda.function_name},period=cdk.Duration.minutes(1)) 
        #if it failed then alarm generate.. 
        #alarm_indication_Failed=cloudwatch_.Alarm(self, 'Alarm_indication_Failed', metric=durationMetric, 
        #threshold=5000, comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 
        #evaluation_periods=1)
        ###Defining alias of  my web health lambda 
        #Web_health_alias=lambda_.Alias(self, "AlaisForWebHealthLambda", alias_name="Web_Health_Alias",
        #version=webhealth_lambda.current_version) 
        #### Defining code deployment when alarm generate .
        #codedeploy.LambdaDeploymentGroup(self, "id",alias=Web_health_alias, alarms=[alarm_indication_Failed])


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