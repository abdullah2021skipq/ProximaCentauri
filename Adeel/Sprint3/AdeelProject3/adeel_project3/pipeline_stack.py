##########################Importing All the nessearry libraries#######################################
from aws_cdk import core
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from aws_cdk import aws_iam
from adeel_project3.adeel_stage import AdeelStage

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        
        ############################## Pipelines Source ###############################
    
        source = pipelines.CodePipelineSource.git_hub(repo_string='adeel2021skipq/ProximaCentauri' ,
        branch = 'main',authentication=core.SecretValue.secrets_manager('Adeel/github/token1'),
        trigger = cpactions.GitHubTrigger.POLL
        )
        
        ############################## Pipelines built ###############################
        
        
        pipelineroles = self.createrole()
        
        synth = pipelines.CodeBuildStep('synth',input = source,
        commands=["cd Adeel/Sprint3/AdeelProject3","pip install -r requirements.txt" , "npm install -g aws-cdk","cdk synth"],
        primary_output_directory = "Adeel/Sprint3/AdeelProject3/cdk.out",
        role = pipelineroles)
        
        ############################## Pipelines update ###############################
        
        pipeline = pipelines.CodePipeline(self,'pipeline',synth = synth)
        
         ############################## beta update ###############################
    
        beta = AdeelStage(self, "BetaStage" , env= {
            'account':'315997497220',
            'region': 'us-east-2'
        })
        
         ############################# prod stage ###############################
        
        prod = AdeelStage(self, "ProdStage" , env= {
            'account':'315997497220',
            'region': 'us-east-2'
        })
        
         ############################## unit test ###############################
        '''' 
        unit_test = pipelines.ShellStep('unit_test',
        commands=["cd Adeel/Sprint3/AdeelProject3","pip install -r requirements.txt" ,
        "pytest unittests","pytest integtests"])
        '''
         ############################## adding stages ###############################
        
        pipeline.add_stage(beta) #pre = [unit_test])
    
        pipeline.add_stage(prod ,
        pre = [pipelines.ManualApprovalStep("PromoteToProd")])
        
        
        
        
    def createrole(self):
        role=aws_iam.Role(self,"pipeline-role",
        assumed_by=aws_iam.CompositePrincipal(
        aws_iam.ServicePrincipal("lambda.amazonaws.com"),
        aws_iam.ServicePrincipal("sns.amazonaws.com"),
        aws_iam.ServicePrincipal('codebuild.amazonaws.com')
        ),
        managed_policies=[
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AwsCloudFormationFullAccess"),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess"),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipeline_FullAccess"),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        ])
        return role