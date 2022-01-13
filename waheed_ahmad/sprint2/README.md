<div id="top"></div>

<h3 align="center">Sprint2 project skipq</h3>

  <p align="center">
    This project is to create multi stage pipeline having beta/gamma and production stages , integrate unit testing and integration stages , and finally add a manual approval step
    <br />

  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Usage</a></l1>
    <li><a href="#contact">Contact</a></li>
    </li>

  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

In this project we are deploying a pipeline that will automate the code deploy and test step Code Pipeline automates the build, test, and deploy phases of your release process every time there is a code change, based on the release model you define. This enables you to deliver features and updates rapidly and reliably.
 `waheed2021skipq`, `ProximaCentauri`




### built-with

* [aws amazon](https://aws.amazon.com/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

You need to goto amazon aws webiste 'https://aws.amazon.com/' and sign up with a IAM user account, 
set up an environment with your required specifications and get started with aws command line interface.



### Prerequisites


* npm
  ```sh
  npm install npm@latest -g
  ```
 * aws latest version
 * for linux
  ```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
  ```
* for windows
    ``` 
    msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
    ```
* Python latest version
  ``` 
  python --version
  ```
### Installation

1. goto aws.amazon.com
2. Clone the repo
   ```
   sh
   git clone 'your repo '
   ```
3. Install NPM packages
   ```
   sh
   npm install
   ```
4. Create pipelinestack
  ```
  Create a stack.py file and create a stack using "https://docs.aws.amazon.com/cdk/api/v1/python/modules.html" as reference
  ```
 
5. Add testing 
  ```
  add testing (unit,integrations) by following reference "https://docs.aws.amazon.com/cdk/api/v1/python/modules.html"
  ```

6.  use this command to bootsrap your pipeline
  ```
  "cdk bootstrap --qualifier <name> --toolkit-stack-name <somename>"
  ```
  
7. Deploy
   ```
   Use cdk deploy 'name' to deploy the pipeline
   ```
  
## Note
Always git push to make the changes work through pipeline




<!-- USAGE EXAMPLES -->
## Usage

Pipeline automates the build, test, and deploy phases of your release process every time there is a code change, AWS CodePipeline is a continuous delivery service you can use to model, visualize, and automate the steps required to release your software. You can quickly model and configure the different stages of a software release process. CodePipeline automates the steps required to release your software changes continuously. For information about pricing for CodePipeline
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [] Simple pipeline
- [] Added beta stage
- [] Testing stages
    - [] Unit testing
    - [] Integration testing
- [] Manual approval step












<!-- CONTACT -->
## Contact

Waheed - [https://twitter.com/BetaOokay]

Project Link: [https://github.com/waheed2021skipq/ProximaCentauri](https://github.com/waheed2021skipq/ProximaCentauri)

<p align="right">(<a href="#top">back to top</a>)</p>



## References

[https://docs.aws.amazon.com/cdk/api/v1/python/modules.html]







