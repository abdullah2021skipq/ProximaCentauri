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
        
       

        
        source= pipelines.CodePipelineSource.git_hub(repo_string ='waheed2021skipq/ProximaCentauri',
        branch= 'main',
        authentication =core.SecretValue.secrets_manager('github-oauthwaheedtokeneast'),
        trigger=cpactions.GitHubTrigger.POLL
        )
        
        
        synth= pipelines.ShellStep('synth', input= source,
        commands=[
            "cd waheed_ahmad/sprint2" , 
<<<<<<< HEAD:waheed_ahmad/sprint2/pcwaheedproject2/pipelinewaheed_stack.py
            "python -m pip install -r requirements.txt", 
=======
            "python -m pip install -r requirements.txt",
>>>>>>> 513f6767ed388e94ed2baa9a16b55b6f28c8fe3d:waheed_ahmad/sprint2/resources/pipelinewaheed_stack.py
            "npm install -g aws-cdk",
            "cdk synth"
            ],
            primary_output_directory= "waheed_ahmad/sprint2")
            
        
                                          
            
        pipeline = pipelines.CodePipeline(self, "waheedMyFirstPipeline",synth = synth,
                                          self_mutation = True)
        #this is beta stage of CI/cD    
        beta= ProductionStage(self,'beta',env={
            'account':'315997497220',
            'region':'us-east-2'
        })
        
        #add tests stages here
        
        # beta= ProductionStage(self,'beta',env={
        #     'account':'315997497220',
        #     'region':'us-east-2'
        # })
        
        pipeline.add_stage(beta)

