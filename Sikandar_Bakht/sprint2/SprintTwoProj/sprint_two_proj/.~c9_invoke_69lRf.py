from aws_cdk import (
    core as cdk
)
from sprint_two_proj.sprint_two_proj_stack import SprintTwoProjStack

class SprintTwoProjStage(cdk.Stage):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        s2_stack = SprintTwoProjStack(self, 'SprintTwoStackInstance')
