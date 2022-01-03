# ProximaCentauri Sprint3
# Public CRUD API Gateway endpoint for web crawler

## Table of contents
* [Project Description](#Project-Description)
* [Technologies](#technologies)
* [Setup](#setup)


## Project Description
According to user requirements, As a web admin I created a public CRUD API Gateway for web crawler to create/read/update/delete teh target list containing the list of website/webpages to crawl.  

## Technologies 
Project is created with follwoing AWS services
* Lambda
* CloudWatch
* DynamoDB
* SNS
* Cloud9
* S3
* CodePipeline
* Secret Manager
* CloudFormation
* API Gateway

## SetUp
To run this project, follow these steps 
* ###  Environment creation on AWS
First of all login in aws.amazon and create a virtual machine and install all requirements.
* ### Store Personal access tokens 
To get access to the Github repository, you have to generate Personal access tokens and then store Personal access tokens in AWS Secret Manager.
* ### Setup Source
At the beginning of the project, it's essential to set up the source. Store the code in your GitHub repository. Add the GitHub repository path in the Source of the pipeline stack.
* ### Clone Local Machine to Github repository
To clone the github repository to local machine run this command
```
$ git clone <github repository url>
```
Then chnage directory to your project folder using this command.
```
$ cd <projectfolder path>
```
if you add any thing to project then commit and push code to github repo using these command. 
 ```
 $ git status
 $ git add .
 $ git commit -m "updated file"
 $git push
 ```
* ### Bootstrap your AWS environments
Before deploying CDK Pipelines, you must bootstrap the AWS environment. An environment is an account/region pair where you want to deploy a CDK stack. Add the Account ID, Region, qualifier name (of your choice), and toolkit name (of your choice) in the command and run this command in the terminal to bootstrap the AWS environment.
```
$ cdk bootstrap aws://<Acount ID>/<Region> --qualifier <name> --toolkit-stack-name <name>
```
Make sure to add your qualifier name in the cdk.json file, add the qualifier name in the following form.
```
"@aws-cdk/core:bootstrapQualifier": "<qualifier name>"
```
* ### Deploy Pipeline 
Once the environment is bootstrap successfully, deploy the pipeline stack using this command. use your pipeline stack name instead of pipeline stack  
```
$ cdk deploy pipelinestack
```
now all required requirements are done on machine. 
* ### CodePipeline
To check that your CDK pipeline is created successfully, open CodePipeline in AWS services  
* ### Upload json file to S3 bucket
When CI/CD pipeline is implemented successfully then upload json file on S3 bucket and check Dynamo DB table. All Url for webpages will be stored into DynamoDB table.
* ### Test API Gateway method
Open API Gateway, and then run method (add input if required for method) and observe chnages in DynamoDB table.  
### Author
Muhammad Irfan Hassan Trainee @skipQ  muhammad.irfan.hassan.s@skipq.org

Thanks! Enjoy:)
