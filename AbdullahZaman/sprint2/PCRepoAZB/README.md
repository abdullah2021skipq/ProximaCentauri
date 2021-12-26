# SPINT2 : Continuous Integration and Continuous Deployment
## Overview
Creating a multi-stage pipeline that has a beta, gemma and production stage using 
AWS CDK. Then adding unit and integration test to the defined stages. The project 
is concluded by automating a rollback to the previous version if the metric is in 
alarm.
![CI/CD](https://github.com/abdullah2021skipq/ProximaCentauri/blob/main/AbdullahZaman/pipeline.jpg)
## Useful Commands
* git add <directory>
* git commit -m "message"
* git push
* git pull
* <p>cdk bootstrap --qualifier <qualifier name> --toolkit-stack-name <name> aws://<accountid>/region</p>
* <p>cdk deploy <pipelineName></p>
* <p>pytest <DirectoryHavingTestFiles><>
## Troubleshooting Instructions
Push the code to GitHub before bootstrapping and deploying afterchanges have been done. 
