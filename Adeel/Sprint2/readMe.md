# Sprint 2

**project tasks**
* Creating a pipeline for the Sprint1
* addingdifferent stage of deployment in pipeline
* Adding unit tests in these stages
* Adding manual choices for the user

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