from aws_cdk import( core as cdk,
pipelines,
aws_codepipeline_actions as captions)

from talha_project.talha_infra_stage import TalhaInfraStage

class TalhaPipelineStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
#creating source
        source=pipelines.CodePipelineSource.git_hub(repo_string="talha2021skipq/ProximaCentauri", branch='main',
        authentication=cdk.SecretValue.secrets_manager('talha_pipeline_sprint2'),
        trigger=captions.GitHubTrigger.POLL)
        
        synth = pipelines.ShellStep("synth", 
            input=source,
            commands=["cd talha/sprint2/talha_project",
                    "pip install -r requirements.txt", 
                    "npm install -g aws-cdk", "cdk synth"
                    #,"npm ci", "npm run build", "npx cdk synth"
                   ],
            primary_output_directory="talha/sprint2/talha_project/cdk.out")
    #Creating a pipeline for Codes, mainly to deploy CDK apps
        pipeline=pipelines.CodePipeline(self, "Pipeline", synth=synth)
        ############################## Defining beta stage to my code pipeline #######################
        beta= TalhaInfraStage(self, "Beta", 
        env={
            'account':'315997497220',
            'region': 'us-east-2'
            })
    
        unit_test=pipelines.ShellStep('unit_test',
            commands=[ "cd talha/sprint2/talha_project",
                    "pip install -r requirements.txt", 
                    "pytest unittests",  "pytest integtests"]    )
        ############ Adding beta stage to pipeline with pre test #####################
        pipeline.add_stage(beta,pre=[unit_test])
        
    ############# Defining and adding production stage in my pipeline with pre  manual approval############## 
        prod= TalhaInfraStage(self, "Prod", 
            env={'account':'315997497220',
                'region': 'us-east-2'} )
        pipeline.add_stage(prod, 
            pre=[  pipelines.ManualApprovalStep("PromoteToProd") ])
        
        
 