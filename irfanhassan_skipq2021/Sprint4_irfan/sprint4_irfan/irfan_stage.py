from aws_cdk import core as cdk

from sprint4_irfan.sprint4_irfan_stack import Sprint4IrfanStack

class IrfanStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        irfan_stack =  Sprint4IrfanStack(self,'irfanSprint4stack')