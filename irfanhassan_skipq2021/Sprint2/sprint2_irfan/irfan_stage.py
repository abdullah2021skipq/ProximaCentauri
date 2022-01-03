from aws_cdk import core as cdk

from sprint2_irfan.sprint2_irfan_stack import Sprint2IrfanStack

class IrfanStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        irfan_stack =  Sprint2IrfanStack(self,'irfanstack')