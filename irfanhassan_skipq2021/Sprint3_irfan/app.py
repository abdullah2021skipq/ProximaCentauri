#!/usr/bin/env python3
import os

from aws_cdk import core 

from sprint3_irfan.irfan_pipeline_stack import IrfanPipelineStack


app = core.App()
IrfanPipelineStack(app, "IrfanskipqPipelineStack",env=core.Environment(account='315997497220', region='us-east-2'))

app.synth()
