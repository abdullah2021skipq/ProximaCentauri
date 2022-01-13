from aws_cdk import (
    core as cdk
)
from sprint_three_proj.sprint_three_proj_stack import SprintThreeProjStack

class SprintThreeProjStage(cdk.Stage):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        s2_stack = SprintThreeProjStack(self, 'SikandarS3Instance')
