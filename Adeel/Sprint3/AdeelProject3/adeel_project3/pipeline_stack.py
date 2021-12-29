##########################Importing All the nessearry libraries#######################################
from aws_cdk import core
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from adeel_project3.adeel_stage import AdeelStage

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        ############################## Pipelines Source ###############################
    
        source = pipelines.CodePipelineSource.git_hub(repo_string='adeel2021skipq/ProximaCentauri' ,
        branch = 'main',authentication=core.SecretValue.secrets_manager('Adeel/github/token1'),
        trigger = cpactions.GitHubTrigger.POLL
        )
        
        ############################## Pipelines built ###############################
        
        
        synth = pipelines.ShellStep('synth',input = source,
        commands=["cd Adeel/Sprint3/AdeelProject3","pip install -r requirements.txt" , "npm install -g aws-cdk","cdk synth","cdk ls"],
        primary_output_directory = "Adeel/Sprint2/AdeelProject3/cdk.out")
        
        ############################## Pipelines update ###############################
        
        pipeline = pipelines.CodePipeline(self,'pipeline',synth = synth)
        
         ############################## beta update ###############################
    
        beta = AdeelStage(self, "Beta" , env= {
            'account':'315997497220',
            'region': 'us-east-2'
        })
        
         ############################# prod stage ###############################
        
        prod = AdeelStage(self, "Prod" , env= {
            'account':'315997497220',
            'region': 'us-east-2'
        })
        
         ############################## unit test ###############################
        
        unit_test = pipelines.ShellStep('unit_test',
        commands=["cd Adeel/Sprint3/AdeelProject3","pip install -r requirements.txt" ,
        "pytest unittests","pytest integtests"])
        
         ############################## adding stages ###############################
        
        pipeline.add_stage(beta, pre = [unit_test])
    
        pipeline.add_stage(prod ,
        pre = [pipelines.ManualApprovalStep("PromoteToProd")])