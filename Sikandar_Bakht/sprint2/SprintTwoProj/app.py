 #!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core
from sprint_two_proj.sikandar_pipeline_stack import SikandarPipelineStack


app = core.App()
print("work please")
SikandarPipelineStack(app, "sikandarpipeline", env=core.Environment(account = '315997497220', region = 'us-east-2'))

app.synth()
