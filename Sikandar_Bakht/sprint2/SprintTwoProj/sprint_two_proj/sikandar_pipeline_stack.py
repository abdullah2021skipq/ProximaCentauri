from aws_cdk import (
    core as cdk,
    pipelines as pipelines,
    aws_codepipeline_actions as cp_actions
)

from aws_cdk import core
from sprint_two_proj.sprint_two_proj_stage import SprintTwoProjStage

class SikandarPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        source = pipelines.CodePipelineSource.git_hub(repo_string = "Sikandar-Bakht/ProximaCentauri",
                                             branch="main",
                                             authentication=cdk.SecretValue.secrets_manager("Sikandar/github/token"),
                                             trigger = cp_actions.GitHubTrigger.POLL
                                             )
        
        synth = pipelines.ShellStep("Synth", input=source,
                                            commands=["cd ./Sikandar_Bakht/sprint2/SprintTwoProj",
                                                      "pip install -r requirements.txt",
                                                      "npm install -g aws-cdk",
                                                      "cdk synth"],
                                            primary_output_directory = "./Sikandar_Bakht/sprint2/SprintTwoProj/cdk.out"
                                            )
        pipeline = pipelines.CodePipeline(self,
                                          'SikandarPipeline',
                                          synth = synth
                                            )
        Beta = SprintTwoProjStage(self, "beta", env = {
                                            'account':'315997497220',
                                            'region' : 'us-east-2'
                                            })

     
