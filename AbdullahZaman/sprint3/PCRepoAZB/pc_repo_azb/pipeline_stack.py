from aws_cdk import(
    core,
    aws_codepipeline_actions as cpactions,
    pipelines
)
from pc_repo_azb.infra_stage import InfraStage

class PipelineStack(core.Stack):
    def __init__(self, scope:core.Construct, id:str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        
        source = pipelines.CodePipelineSource.git_hub(repo_string="abdullah2021skipq/ProximaCentauri", branch='main',
                authentication=core.SecretValue.secrets_manager('Abdullah_token'),
                trigger=cpactions.GitHubTrigger.POLL
                )
                
        
        synth = pipelines.ShellStep('synth', input=source,
                commands = [
                "cd AbdullahZaman/sprint3/PCRepoAZB", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
            primary_output_directory="AbdullahZaman/sprint3/PCRepoAZB/cdk.out"
                )
                
        
        pipeline = pipelines.CodePipeline(self, 'Pipeline', synth=synth)
        
        
        beta = InfraStage(self, "AbdullahBetaSPRINT3", env={
        'account': '315997497220',
        'region': 'us-east-2'
        })
        
        production = InfraStage(self, "AbdullahProductionSPRINT3", env={
        'account': '315997497220',
        'region': 'us-east-2'
        })
        
        unitTest = pipelines.CodeBuildStep(
            'unit_tests',input=source,
            commands=["cd AbdullahZaman/sprint3/PCRepoAZB/","pip install -r requirements.txt", "npm install -g aws-cdk", "pytest unit_tests"]
            )
            
        integrationTest = pipelines.CodeBuildStep(
            'integration_tests',input=source,
            commands=["cd AbdullahZaman/sprint3/PCRepoAZB/","pip install -r requirements.txt", "npm install -g aws-cdk", "pytest integration_tests"]
            )
        
        pipeline.add_stage(beta, pre=[unitTest] ,post=[integrationTest])
        pipeline.add_stage(production)
        