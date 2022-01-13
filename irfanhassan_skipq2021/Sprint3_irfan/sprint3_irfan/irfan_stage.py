from aws_cdk import core as cdk

from sprint3_irfan.sprint3_irfan_stack import Sprint3IrfanStack

class IrfanStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        irfan_stack =  Sprint3IrfanStack(self,'irfanSprint4stack')