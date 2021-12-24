from aws_cdk import core as cdk

from skipqproject.pipeline_stage import PipelineStage
from aws_cdk import pipelines
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as cpactions
from aws_cdk import aws_iam

class PipelinesStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
                                                   #owner/reponame
        source=pipelines.CodePipelineSource.git_hub("Ayesha-zakria/ProximaCentauri", "main",
            authentication=cdk.SecretValue.secrets_manager('ayeshazakria'),
            trigger=cpactions.GitHubTrigger.POLL
            )
        
        pipelineroles = self.createrole()
            
        synth=pipelines.CodeBuildStep("Synth",
                input=source,
                commands=["cd Ayeshazakria/skipqsprint2", "pip install -r requirements.txt", "npm install -g aws-cdk","cdk synth"
                ],
                primary_output_directory='./Ayeshazakria/skipqsprint2/cdk.out',
                role=pipelineroles
            )
        pipeline=pipelines.CodePipeline(self, 'ayeshapipeline',synth=synth)
        
        beta = PipelineStage(self, "ayeshabetastage",
        env = {
            'account':'315997497220',
            'region' : 'us-east-2'
         })
       
        pipeline.add_stage(beta)
        
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
        