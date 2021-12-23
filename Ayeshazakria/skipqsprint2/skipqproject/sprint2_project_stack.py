from aws_cdk import (
    core as cdk
)


from aws_cdk import core


class SprintTwoProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print("Sprint 2 Project stack created")