from aws_cdk import (
    core as cdk,
   # pipelines,
   # aws_codepipeline_actions as cpactions
    # aws_sqs as sqs,
)
from skipqproject.pipeline_stage import PipelineStage
from aws_cdk import pipelines
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as cpactions




class PipelinesStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
                                                   #owner/reponame
        source=pipelines.CodePipelineSource.git_hub("Ayesha-zakria/ProximaCentauri", "main",
            authentication=cdk.SecretValue.secrets_manager('ayeshazakria'),
            trigger=cpactions.GitHubTrigger.POLL
            )
        synth=pipelines.ShellStep("Synth",
                input=source,
                commands=["cd Ayeshazakria/skipqsprint1", "pip install -r requirements.txt", "npm install -g aws-cdk","cdk synth"
                ],
                primary_output_directory='Ayeshazakria/skipqsprint1/cdk.out'
            )
            
            
        pipeline=pipelines.CodePipeline(self, 'ayeshapipeline',synth=synth)
        
       
       
        pipeline.add_stage(PipelineStage(self, 'ayeshabetastage'))
        