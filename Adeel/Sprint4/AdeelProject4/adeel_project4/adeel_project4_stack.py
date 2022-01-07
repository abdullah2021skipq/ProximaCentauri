##########################Importing All the nessearry libraries#######################################
from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as event_,
    aws_events_targets as targets_,
    aws_lambda_event_sources as sources_,
    aws_s3 as s3,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db,
    aws_codedeploy as codedeploy,
    aws_apigateway as apigateway,
    aws_amplify as amplify,
    aws_s3_assets as s3_assets
)
from constructs import Construct
from resources1 import constants1 as constants
from resources1.bucket import Bucket as bo  
import resources1.db_ReadWrite_handler as dynamo_RW

class AdeelProject4Stack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        ############################## Define lambda role and lambda functions###############################

        lambda_role= self.create_lambda_role()
        WH_lamda = self.create_lambda('FirstHellammbda',"./resources1/",'WH_lambda.lambda_handler',lambda_role)
        
        
         ############################## Schedule and Role functions for lambda ############################### 
         
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = WH_lamda)
        our_rule = event_.Rule(self, id = "MonitorWebHealthMAtrix",enabled = True, schedule= lambda_schedule,targets = [lambda_target] )
        
        
         ################################## creating amplyfy resources for react app ################
         
        api_asset = s3_assets.Asset(self, "AppBuiltAsset",
        path="build.zip")
        
        amplify_app = amplify.App(self, 'AdeelApp',role=lambda_role)
        branch = amplify_app.add_branch('dev')
        branch.add_environment(name = 'Bucket', value = 'adeelskipq')
        ''''
        source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="adeel2021skipq",
        repository="adeel2021skipq/ProximaCentauri",
        oauth_token=cdk.SecretValue.secrets_manager("Adeel/github/token1")),
        '''
        
         
        
        
         ################################## creating table for urls to read from ###########
        
        urls_table=self.create_table(id='Urls',
        key=db.Attribute(name="Links", type=db.AttributeType.STRING))
        db_lambda_role = self.create_db_lambda_role()
        s3_db_lamda = self.create_lambda('thirdHellammbda',
                      "./resources1/",'db_s3_lambda.lambda_handler',db_lambda_role)
        
        
        ##################################### Creating invoke source for lambda file ############
        
        bucket = s3.Bucket(self, "BucketForURLs")
        s3_db_lamda.add_event_source(sources_.S3EventSource(bucket,
        events=[s3.EventType.OBJECT_CREATED],
        filters=[s3.NotificationKeyFilter(suffix=".json")]
        ))
        
        ########## Givivng urls table full access and passing its name to different lambdas #######
        
        urls_table.grant_full_access(s3_db_lamda)
        s3_db_lamda.add_environment(key = 'table_name', value = constants.URLS_TABLE_NAME)
        WH_lamda.add_environment(key = 'table_name', value = constants.URLS_TABLE_NAME)
        
        
        ############# Crreating Api gate way lambda and passing table name to it ############
        
        
        api_lamda = self.create_lambda('ApiHellammbda',
                      "./resources1/",'api_lambda.lambda_handler',db_lambda_role)
        api_lamda.add_environment(key = 'table_name', value = constants.URLS_TABLE_NAME)
        
        
        ################################# creating API gateway ###################
        
        
        api_lamda.grant_invoke( aws_iam.ServicePrincipal("apigateway.amazonaws.com"))
        urls_table.grant_read_write_data(api_lamda) 
        
        #Create API gateway
        api = apigateway.LambdaRestApi(self, "Adeel_API_gateway",
        handler= api_lamda
        )
        
        items = api.root.add_resource("items")
        items.add_method("GET") # GET /items
        items.add_method("PUT") #  Allowed methods: ANY,OPTIONS,GET,PUT,POST,DELETE,PATCH,HEAD POST /items
        items.add_method("DELETE")
        
        
        ############################## Creating Dynamo table and giving it Premission ###############################
         
         
        dynamo_table=self.create_table(id='BDtable',
        key=db.Attribute(name="Timestamp", type=db.AttributeType.STRING))
        db_lamda = self.create_lambda('secondHellammbda',"./resources1/",'dynamo_lambda.lambda_handler',db_lambda_role)
        dynamo_table.grant_full_access(db_lamda)
        db_lamda.add_environment('table_name', dynamo_table.table_name)
        
        
         ############################## Subscriptions ###############################
        
        topic = sns.Topic(self,'WHtopic')
        topic.add_subscription(subscriptions_.EmailSubscription('adeel.shahzad.s@skipq.org'))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=db_lamda)) 
        
         ############################## Alarms on cloud watch ###############################
        
        ######data from bucket as list ############
        
        Url_Monitor = bo('adeelskipq','urls.json').bucket_as_list()
        
        ######## data from table as list########
        
        links = dynamo_RW.ReadFromTable(constants.URLS_TABLE_NAME)
        b=1
        for url in links:
            
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
        
        ''''
        WH_alias=self.create_alais(id = "AlaisForLambda",name = "AdeelLambdaVersion",
        version = WH_lamda.current_version)
        #### Defining code deployment group
        codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",alias=WH_alias,
        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
        alarms=[alarm_fail])
        '''
        ##############################  role for Cloud watch ###############################
        
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self,"lambda-role",
        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies = [aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"), 
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('AdministratorAccess-Amplify')
        ])
        return lambdaRole
        
         ############################## role for dynamo ###############################
        
    def create_db_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role-db",
                        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
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