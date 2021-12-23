import aws_cdk.core as cdk
from constructs import Construct
from skipqproject.pipeline_lambda import PipelineLambda

class PipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaStack = PipelineLambda(self, "LambdaStack")