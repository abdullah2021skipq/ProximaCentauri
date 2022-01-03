from aws_cdk import core as cdk

from aws_cdk import core
from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from pcwaheedproject2.pipelinewaheed_stage import ProductionStage

class waheedsprint(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
       
    ##defining source here where the code should be pulled from for pipeline
        
        source= pipelines.CodePipelineSource.git_hub(repo_string ='waheed2021skipq/ProximaCentauri',
        branch= 'main',
        authentication =core.SecretValue.secrets_manager('github-oauthwaheedtokeneast'), #token in secrets manager
        trigger=cpactions.GitHubTrigger.POLL
        )
        
        
        synth= pipelines.ShellStep('synth', input= source,
        commands=[
            "cd waheed_ahmad/sprint2" ,
            "python -m pip install -r requirements.txt", 
            "npm install -g aws-cdk",
            "cdk synth"
            ],
            primary_output_directory= "waheed_ahmad/sprint2/cdk.out")
            
        
                                          
            
        pipeline = pipelines.CodePipeline(self, "waheedMyFirstPipeline",synth = synth,
                                          self_mutation = True)
        #this is beta stage of CI/cD    
        beta= ProductionStage(self,'beta',env={
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        gemma = ProductionStage(self,'gemma',env={
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        prod = ProductionStage(self,'prod',env={
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        
        
        ### Tests stage of our pipeline
        unit_test=pipelines.ShellStep('unit_test',
            commands=[ "cd waheed_ahmad/sprint2",
                    "pip install -r requirements.txt",
                    "pytest unittests"]    )
        
        integ_test=pipelines.ShellStep('unit_test',
            commands=[ "cd waheed_ahmad/sprint2",
                    "pip install -r requirements.txt","pytest integtest"]    )
        
        pipeline.add_stage(beta)
        #pipeline.add_stage(gemma , pre=[pipelines.ManualApprovalStep("promotetoproduction")])
        pipeline.add_stage(gemma, pre= [unit_test],post=[pipelines.ManualApprovalStep("promotetodeproduction")])  
        # if i add pre manual approval so it gets paused for human manual  approval tll then it is not deployed
        pipeline.add_stage(prod, pre=[integ_test],post=[pipelines.ManualApprovalStep("promotetodeployment")]) 

