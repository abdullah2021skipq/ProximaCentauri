from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_
)


class IrfanSkipQProject1Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        hello_lamda = self.create_lambda('FirstHellammbda',"./resources",'lambda.lambda_handler')
        
        
    def create_lambda(self,id, asset, handler):
        return lambda_.Function(self, id,runtime=lambda_,runtime.PYTHON_3_8,handler=handler,code=lambda_.Code.asset(asset))