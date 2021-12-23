import aws_cdk.core as cdk
from constructs import Construct
from skipqproject.sprint2_project_stack import SprintTwoProjectStack

class PipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sprint2_Stack = SprintTwoProjectStack(self, "sprint2projectstackinstance")