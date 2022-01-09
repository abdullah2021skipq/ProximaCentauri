# Sprint 4

## project discription
**__Build a Front-End user-interface for the CRUD API Gateway using ReacUS. The user interface should allow users to see and search the database (DynamoDB) and should load URLs with pagination. Login should be enabled through React with authentication using AWS Cognito or equivalent OAuth method. The React app can be rendered with an AWS Lambda Function. Use the library of foundational and advanced components and design system in Chakra UI to develop your React application. .__**

## Concepts:

* Learn how to create a Front-End app with ReacUS 
* Learn how to enable authentication using OAuth method
* Write accessible React apps using readily available UI libraries. 

 
## Techonologies

* ReactJS
* Javasript
* ChakraUI
* AWS Amplify
* AWS cognito
* AWS API gateway

## project tasks
* Create a ReactJS web applcation
* Connect the app to API and impliment pagination
* Deploy the app to S3
* And a sing in, sign up method on app.

# How to Run

## Clone

**First clone all the files from git hub repository using this command.**

> git clone https://github.com/adeel2021skipq/ProximaCentauri.git

**Go to project directory**

> cd ProximaCentauri/Adeel/Sprint4/AdeelProject4

## Virtual environment

**Go to virtual environment using command**

> source .venv/bin/activate

## Bootstrap

**Bootstrap the code using that command**

> cdk bootstrap aws://315997497220/us-east-2 --qualifier adeel123 --toolkit-stack-name adtoolkit

## Deploy

> cdk deploy AdeelPipelineStack3

# App
**After deloyment is coplete go to AWS apmlify and onpen the URL assigned to the app. Open the URL signUp using email and enjoy**