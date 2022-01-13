##------------Pipeline stack Code------------------------##
from aws_cdk import (
    core,
    pipelines,
    aws_codepipeline_actions as cpactions
)
from sprint3_irfan.irfan_stage import IrfanStage
class IrfanPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
#########  adding source to piepline (GitHub respository) ################################################
        source = pipelines.CodePipelineSource.git_hub(repo_string = "muhammadskipq2021/ProximaCentauri",branch = "main",
                           authentication = core.SecretValue.secrets_manager("Irfan_sprint2_secretkey"),
                           trigger = cpactions.GitHubTrigger.POLL)
                           

##########  Installing the requirement and Build the Source ##############################################
        synth = pipelines.ShellStep('synth', input= source,
                commands = ["cd irfanhassan_skipq2021/Sprint3_irfan","pip install aws-cdk.aws_cloudwatch_actions==1.135.0", 
                            "pip install -r requirements.txt ","npm install -g aws-cdk","cdk synth" ],
                            primary_output_directory = "irfanhassan_skipq2021/Sprint3_irfan/cdk.out"
                            )
        pipeline = pipelines.CodePipeline(self,'pipeline',synth=synth)
        
        
########   Adding Beta Stage with Unit Test and Initgration Test ###########################################
        betaStage = IrfanStage(self, "BetaStag", env = { 'account': '315997497220', 'region': 'us-east-2'})
        #test = pipelines.ShellStep('unit_and_Integration_test_',commands=["cd irfanhassan_skipq2021/Sprint3_irfan", "pip install -r requirements.txt",
        #"pip install pytest","pip install requests","pytest unittest"])#,"pytest Intigration"])
        pipeline.add_stage(betaStage)#, post = [test])
    
        
#######  Addign Prodcution stage with mannaul approval in Pipeline  #######################################3
        #prodstage= IrfanStage(self, "ProdStage", env={'account':'315997497220','region': 'us-east-2'} )
        #pipeline.add_stage(prodstage, pre=[  pipelines.ManualApprovalStep("PromoteToProd") ])
        
      
        