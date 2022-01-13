

# Sprint3: Build CRUD API Gateway for Web Crawler 
## Table of Contents

1. [Project Summary](#Project-Summary)

2. [Services Covered](#Services-Covered)

3. [Installation Guide](#Installation-Guide)

4. [Project Status](#Project-Status)

5. [Author](#Author)

## Project Summary 

In the sprint3 at skipQ, I created a public CRUD API gateway so that user can Read, Write, Update or Delete URLs in dynamodb table through the API Gateway. I have made an update in the existing web monitoring system, that is to read web URLs from Dynamodb table instead of reading from S3 bucket.
Moreover, I have created some unit tests in beta stage of the code pipeline while integration tests were added as post-beta step. 
## Services Covered

1. AWS Api Gateway
2. Dynamodb
3. AWS Cloudwatch
4. S3 buckets
5. AWS lambda
6. AWS SNS
7. AWS events
8. AWS events target
9. AWS Pipelines
10. AWS Codepipeline Actions

## Installation Guide

Follow these easy steps to set up the environment and run the project:

1. Run the following command to clone the repo:
	
	    `git clone https://github.com/talha2021skipq/ProximaCentauri.git`

2. Land in my project directory by running the command:

	   `cd ProximaCentauri/talha/sprint3/talha_project`

3. Bootstrap the environment by using following command:

           `cdk bootstrap aws://315997497220/us-east-2 --qualifier mtalhas --toolkit-stack talhastoolkit`
 	- Make sure to specify qualifier name as talha, if you change it then you will have to replace talha with your qualifier's name on line number 24 in `cdk.json` file as shown below:

 			`"@aws-cdk/core:bootstrapQualifier": "mtalhas"`
4. The environment is bootstrapped, now it's time to deploy the pipeline. Deploy the pipeline by using the below mentioned command but make sure you are in the same directory where the `app.py` is located.  
          
           `cdk deploy Sprint3TalhaPipelineStck`
5. Go to the console and open code pipelines to see the pipeline fully working. Search the pipeline by name 'Sprint3TalhaPipelineStck'. 
6. Go to the console and open API Gateway to test and run the API. Open TalhasAPI from APIs Dashboard. Click on 'ANY' Method to open the created API Gateway for web crawler.
7. Now click on Test to run the API and then select any method from the drop down menue to perform CRUD operations.

## Project Status

Completed!

## Author

 Talha Naeem 
DevOps Trainee @skipQ 
talha.naeem.s@skipq.org

Thanks! Enjoy:)

