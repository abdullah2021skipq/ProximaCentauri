# Sprint 3

## project discription
**__emitct Build a public CRUD API Gateway endpoint for the web crawler to create/read/update/delete the target list containing the list of websites/webpages to crawl. First, move the json file from S3 to a database (DynamoDB). Then implement CRUD REST commands on DynamoDB entries. Extend tests in each stage to cover the CRUD operations and DynamoD8 read/write time. Write API documentation and commit to github. Manage README files and runbooks in markdown on GitHub.__**

## Concepts:

* Learn AWS Services: API Gateway, DynamoDB
* Write -a RESTful API Gateway interface for web crawler CRUD operations
* Write a Python Function to implement business logic of CRUD into DynamoDB
* Extend tests and prod/beta Cl/CD pipelines in CodeDeploy / CodePipeline
* Use Cl/CD to automate multiple deployment stages (prod vs beta
 
## Techonologies

* Code PipeLine
* CloudFormation
* Lambda
* DynamoDB
* CodeDEployment
* CloudWatch
* 

## project tasks
* Creating a API gateway for the Sprint2
* Taking data from S3and moving it to the dynamo table
* Seeting Alarms on dynamo data
* Adding deleting and getting data from table using API
* Adding more tests

## Clone

**First clone all the files from git hub repository using this command.**

> git clone https://github.com/adeel2021skipq/ProximaCentauri.git

**Go to project directory**

> cd ProximaCentauri/Adeel/Sprint2/adeeldynamoDB

## Virtual environment

**Go to virtual environment using command**

> source .venv/bin/activate

## Bootstrap

**Bootstrap the code using that command**

> cdk bootstrap aws://315997497220/us-east-2 --qualifier adeel123 --toolkit-stack-name adtoolkit

## Deploy

> cdk deploy AdeelPipelineStack3