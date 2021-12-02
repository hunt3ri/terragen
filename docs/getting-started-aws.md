# Getting Started with Terragen on AWS
Here we outline how you can use Terragen to manage your infrastructure on AWS

## Installation
To install Terragen, run the following from the command line:
```commandline
pip install terragen
```

## Creating a AWS cloud environment
Terragen expects to run from within a directory which has both a `config` directory containing all the Terragen config and a `modules` directory containing your Terraform modules, like this:

```commandline
|-terragen
|----config
|--------config.yaml
|----modules
```
The quickest way to start is to clone our example repo:
```commandline
git clone https://github.com/hunt3ri/terragen-example-configs.git
```

Your Terragen workspace is now ready to go

## Configuring your AWS environment
### Credentials
Terragen simply wraps the Terraform CLI

## Running Terragen
### First Run
#### Resolve Our Config
For our first run lets first check that Terragen can resolve the config we created above.  We need to tell Terragen where the config directory is located using the `--config-dir` switch or `-cd` for short, as follows:
```commandline
terragen --config-dir ./config --cfg job --resolve
```

If successful the entire YAML of our configuration and base classes will be echod to the screen

#### Running in Debug Mode
Next we are going to run with Debug set to True, this will generate all our Terraform modules with our configuration output as .tfvars file in the `outputs` directory, as follows:
```commandline
terragen -cd ./config build.debug=True
```

#### Checking our generated Terraform modules in outputs dir
Everytime you run Terragen it creates a date/time stamped directory called outputs.  If the above step was successful you should now have a new directory called outputs with your Terraform modules located similar to this (adjusted to date/time you ran Terragen)

```commandline
|-terragen
|----config
|----modules
|----outputs
|--------2021-12-01
|------------23-52-57
|----------------AWSProvider
|--------------------dev
|------------------------ec2
|------------------------key_pairs
|------------------------vpc
```

#### Applying our Infrastructure
If we're happy with the generated Terraform modules we can apply it, obviously with debug set to False, as follows:

TODO - Use base Ubuntu Image in example

```commandline
terragen -cd ./config build.debug=False
```

## Seperately creating Shared and App specific Infra
Terragen allows you to create and configure shared pieces of infrastructure like VPCs, KeyPairs, Security Groups and Project/Application infrastructure like ASGs, EC2 instances all from one workspace.  Click the links to get clarifications on what we mean by shared and project specific infrastructure.  