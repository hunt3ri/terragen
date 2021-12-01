# Getting Started with Terragen on AWS
Here we outline how you can use Terragen to manage your infrastructure on AWS

## Installation
To install Terragen, run the following command from the command line:
```commandline
pip install terragen
```

## Creating a AWS cloud environment
Terragen allows you to create and configure shared pieces of infrastructure like VPCs, KeyPairs, Security Groups and Project/Application infrastructure like ASGs, EC2 instances all from one workspace.  Click the links to get clarifications on what we mean by shared and project specific infrastructure.  

Terragen expects to run from within a directory which has both a `config` directory containing all the Terragen config and a `modules` directory containing your Terraform modules, like this:

```commandline
|-terragen
|----config
|--------config.yaml
|----modules
```
The quickest way to start is to clone our example repo here

## Configuring your AWS environment
### Credentials
Terragen simply wraps the Terraform CLI