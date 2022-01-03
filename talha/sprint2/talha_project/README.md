

# Sprint2: Creating CI/CD Pipeline 
## Project Summary 

In the sprint2 at skipQ, I created a CI/CD pipeline with beta and production stage. In the pipeline, the first step is to set up the source and then build environment for it to get deployed. After that, I embedded the feature of automatic update in pipeline on the trigger or change in the source repository. After the setup, the code is built and deployed in beta stage, where I have added pre-unit tests. In the last, I have added a prod stage in the same region with manual approval. I had already designed a web health monitoring system, that will periodically monitor the web health metrics, so in sprint 2 I added another feature, that is to raise an alarm on the metric(Duration) of my lambda function and then raise an alarm after a specific threshold. An alias for my web health lambda function is created. And upon the alarm, I have shifted the traffic to the alias of that lambda function.
## Services Covered

1. AWS Dynamodb
2. AWS Cloudwatch
3. S3 buckets
4. AWS lambda
5. AWS SNS
6. AWS events
7. AWS events target
8. AWS Pipelines
9. AWS Codepipeline Actions
## Installation Guide

Follow these easy steps to set up the environment and run the project:

1. Run the following command to clone the repo:
	
	    `git clone https://github.com/talha2021skipq/ProximaCentauri.git`

2. Land in my project directory by running the command:

	   `cd ProximaCentauri/talha/sprint2/talha_project`

3. Bootstrap the environment by using following command:

           `cdk bootstrap aws://315997497220/us-east-2 --qualifier talha --toolkit-stack talhastoolkit`
 	- Make sure to specify qualifier name as talha, if you change it then you will have to replace talha with your qualifier's name on line number 24 in `cdk.json` file as shown below:

 			`"@aws-cdk/core:bootstrapQualifier": "talha"`
4. The environment is bootstrapped, now it's time to deploy the pipeline. Deploy the pipeline by using the below mentioned command but make sure you are in the same directory where the `app.py` is located.  
          
           `cdk deploy TalhaPipelineStack`
5. Go to the console and open code pipelines to see the pipeline fully working. Search the pipeline by name 'TalhaPipelineStck'.  

## Project Status

Completed!

## Author

 Talha Naeem 
DevOps Trainee @skipQ 
talha.naeem.s@skipq.org

Thanks! Enjoy:)

