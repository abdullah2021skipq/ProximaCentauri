import boto3
import constants1 as constants

class cloudWatchPutMetric:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
        
    def put_data(self, nameSpace, metricName, dimensions, value):
        response = self.client.put_metric_data(
            Namespace = nameSpace,
            MetricData=[
            {
                'MetricName':metricName, 
                'Dimensions':dimensions,
                'Value':value
            }
        ])