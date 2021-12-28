import boto3
import constant as constants
class Cloudwatchputmetrics:
    def __init__(self):
        self.client= boto3.client("cloudwatch")
    
    def put_data(self, nameSpace,metricName,dimensions,values):
        response= self.client.put_metric_data(
             Namespace=nameSpace,
             MetricData=[
                 {
                     "MetricName":metricName,
                     "Dimensions":dimensions,
                     "Value":  values
                 }
                 ]
            )