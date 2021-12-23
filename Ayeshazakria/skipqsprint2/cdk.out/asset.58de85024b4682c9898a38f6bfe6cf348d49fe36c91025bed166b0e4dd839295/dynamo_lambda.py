import datetime
import urllib3
import constant as constants
from cloudwatch import Cloudwatchputmetrics

def lambda_handler(event,context):
    print(event)
    print(context)
    # why here.