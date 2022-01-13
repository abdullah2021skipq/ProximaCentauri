# ProximaCentauri Sprint2
# Continuous integration and delivery (CI/CD) using CDK Pipelines

## Table of contents
* [Project Description](#Project-Description)
* [Technologies](#technologies)
* [Setup](#setup)


## Project Description
In this project, I create CI/CD pipeline having Beta and Prod stage using CDK. I set up the source from my Github repository for CI/CD Pipeline. CI/CDpipeline will get the web health monitor application's source code from the GitHub repository and will automate the process of building, testing, and deploying the application. First, it installs requirements for source code and then synth the code. In the Beta stage,  it runs the unit test and integration test. After passing through the unittest, it deploys the source code. In Prodstage, it asks for manual approval then deploys the source code. When adding new stacks/stages or updating anything in the application, CI/CD pipeline automatically reconfigures itself to deploy those new stages and stacks.

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
* ### Results
Wwhen CI/CD pipeline is implemented successfully then open cloud watch to observe the web health of URLs and then check Email and dynamo DB Tables to see details of the alarm notifications.
### Author
Muhammad Irfan Hassan Trainee @skipQ  muhammad.irfan.hassan.s@skipq.org

Thanks! Enjoy:)
