#!/usr/bin/env python3
import os
# from flask import Flask
# import logging as logger
from aws_cdk import core as cdk
from aws_cdk import core
from sprint3.pipelinewaheed_stack import waheedsprint2

# logger.basicConfig(level="DEBUG")
# flaskAppInstance= Flask(__name__)
# if(__name__)== '__main__':
#     logger.debug("starting the application")
#     flaskAppInstance.run(host="0.0.0.0", port=5000, debug = True , use_reloader= True)

app = core.App()
waheedsprint2(app, "waheedsprint2", env=core.Environment(account='315997497220', region='us-east-2'))

app.synth()
