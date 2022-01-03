
# Sprint3: Updating URLs of Health Monitor webcrawler via CRUD operations using REST API
## Table of Contents

1. [Project Summary](#Project Description)
2. [AWS Services Used](#SAWS Services Used)
3. [Installation Guide](#Instructions)
5. [Author](#Author)

## Project Description

Creating a RESTful API implementing CRUD methods of GET, POST, PUT and DELETE to retrieve URLs from S3 bucket and also adding more urls based on request sent via endpoint request URL. Successfully implemented the API while incorporating the functions from previous sprint.

## Services Covered

1. AWS Lambda
2. AWS DynamoDB
3. AWS API Gateway
4. AWS Code Deploy
5. AWS Pipeline

## Instructions:

To get this repo up and running follow these steps:

1. cd to your desired folder and run this command in terminal
	
	    `git clone https://github.com/Sikandar-Bakht/ProximaCentauri.git`

2. cd to the project directory using this command:

	   `cd ./ProximaCentauri/Sikandar_Bakht/sprint3/SprintThreeProj`

3. (Optional) Bootstrap the environment by running the following command.

     `cdk bootstrap --qualifier "sikandars3" --toolkit-stack-name "sikandartoolkit" --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess 315997497220/us-east-2`
    The `qualifier` and `toolkit-stack-name` are variable parameters, you can change them to whatever you like. If you change qualifier name, change the same in `cdk.json` file
    in the project directory as well.

4. In the `./SprintThreeProj` directory, run the following command in terminal:
    
       `cdk deploy sikandarpipeline`
       
5. Manually approve the prod stage in CodePipeline
       
6. The pipeline is created and two stacks by names starting with 'beta' and 'prod' are created. Go to AWS API Gateway and search for API with the query 'Sikandar';
   two of them should come up.

7. Select first one, go to stages in the left hand menu and copy the URL endpoint displayed.
8. Go to your favorite API tester (I use Postman) and try any of the methods in the repo.

## Author

Sikandar Bakht

For queries, reach out to me at:
sikandar.bakht.s@skipq.org

