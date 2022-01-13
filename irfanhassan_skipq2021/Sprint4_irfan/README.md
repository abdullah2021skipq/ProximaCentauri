# ProximaCentauri Sprint4
# Frond-End User Interface for CRUD API Gateway

## Table of contents
* [Project Description](#Project-Description)
* [Technologies](#technologies)
* [Setup](#setup)


## Project Description
Building a Front-End user interface for CRUD API Gateway using React JS and Chakra UI. This React APP will allow the user to search and get URLs from the Dynamo DB table. The React APP will be integrated into CRUD API Gateway and will send GET requests. Log in access will be enabled using the OAuth method. 

## Technologies 
Project is created with follwoing AWS services
* Node JS 
* Visual Studio Code 
* React JS 
* Chakra UI 
* AWS Amplify


## SetUp
DO following steps to complete the project. 
Install Node JS and visual studio code.
Run command to create App
```
$ npm create-react-app my-app
```
Change directory to my-app using this command
```
$ cd my-app
```
Run this command to install Chakra UI Library
```
$ npm i @chakra-ui/react @emotion/react@^11 @emotion/styled@^11 framer-motion@^5
```	
Now remove all files from the src folder except App.js and index.js
Write code in App.js for react app. 
Now check your app by running this command
```
$ npm start
```
Once your app is done. Build an app using this command. 
```
$ npm run build
```
Make zip folder from build folder and upload to S3 Bucket/GitHub Repo. 
Go to AWS Amplify service and deploy the zip file from S3 Bucket/GitHub Repo.
Go to URL and test your App.
  
### Author
Muhammad Irfan Hassan Trainee @skipQ  muhammad.irfan.hassan.s@skipq.org

Thanks! Enjoy:)
