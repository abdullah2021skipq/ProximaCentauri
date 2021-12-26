
# Welcome to Multistage pipelined webcrawler app!

This project is a continuation of Webhealth monitoring crawler from Sprint 1. Here we learn the basics of Continuous Integration and Delivery, where we integrate new changes into existing application and provide it with the required resources as needed.

## To run this project, follow these steps:

Generate a clean environment (recommended)

Clone this repository in your environment.

Navigate to SprintTwoProj directory by using the command `cd ./ProximaCentauri/Sikandar_Bakht/sprint2/SprintTwoProj`

Create a new python virtual environment and activate it by running these commands: `python -m venv .venv` and `source .venv/bin/activate`

If this is your first time running this project or bootstrapping, you need to follow these steps:
  1) In SprintTwoProj, open the `cdk.json` file and add the following lines to the context dictionary:
        
       `"@aws-cdk/core:newStyleStackSynthesis": true,`
       `"@aws-cdk/core:bootstrapQualifier": "sikandars2"`
       
  2) In the terminal, run the command `export CDK_NEW_BOOTSTRAP=1`
  3) In the terminal, run the command 
 
      `cdk bootstrap --qualifier <qualifier> --toolkit-stack-name <toolkit-stack-name> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess <account id>/<region>`
  
If everything went well, your environment should now be bootstrapped.
Now, just run `cdk deploy sikandarpipeline` and your pipeline should be deployed.
