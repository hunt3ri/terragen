# Getting Started with Terragen on AWS
Here we outline how you can use Terragen to manage your infrastructure on AWS

## Installation
To install Terragen, run the following from the command line:
```commandline
pip install terragen
```

## Terragen Workspace
Next we can now define our Terragen workspace.  This is the location where Terragen will run, read your config and generate your Terraform Modules

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

## AWS Authentication and Terraform Statefile
To enable Terragen to run Terraform and for Terraform to apply your modules you are going to have to define an AWS shared credentials file and a S3 Bucket to store your Terraform statefile.  Once defined we can supply Terragen with your credentials name, and bucket name and let Terraform do the rest.  Details below

### S3 Bucket
Terragen expects your AWS Statefile to be stored in S3.  [Follow this link for best practice on defining your bucket.](https://www.terraform.io/docs/language/settings/backends/s3.html)  We'll see shortly how to supply this to Terragen

### AWS Credentials

To enable Terragen to run the Terraform CLI, Terragen expects you to define an AWS shared credentials file (see links below).  Again we'll see shortly how to supply the detail to Terragen 

* [AWS Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
* [Terraform Shared Credentials File](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#shared-credentials-file)

### Security
Terragen NEVER accesses any of your credentials



## Running Terragen
We are now ready to define our Terragen config.yaml and create our first cloud infrastructure.
### config.yaml
You can store your config in any named YAML file, but for now we're going to use config.yaml.
#### defaults
#### build
#### environment 
Environment Details goes here


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