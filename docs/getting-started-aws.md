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


## Configuring Terragen
We are now ready to look at the Terragen config.yaml and to define our first cloud infrastructure.

### config.yaml
You can store your config in any named YAML file, but for now we're going to use the default config.yaml.  config.yaml is split into 3 key sections:

#### 1. defaults
`defaults` is a list telling Terragen how to compose the final config object.  Here we define the namespace of the final config object which we will see below.  The namespace is split into two sections:

* `shared` - Within this namespace we define pieces of infrastructure that may be shared by multiple apps, for example VPCs, Databases, KeyPairs etc
* `apps` - App specific infrastructure - only relates to the application you are deploying

By splitting the namespace in half like this we can manage shared and app specific infra separately at build time.  For example, only tearing down our app, but leaving shared infra like the database alone.

In our example app you can see the VPC is shared, but the EC2 instance is specific to the app. eg we may want multiple apps to share this VPC.

```yaml
defaults:
  # Shared Infrastructure
  - aws/shared/vpcs@shared.vpc.simple_vpc: simple_vpc

  # Apps
  - aws/apps/sandbox@app.ec2.sandbox: sandbox
```

#### 2. environment 
`environment` is where you can put environment specific configuration.  Eg in DEV you may only want a t3.small instance, but your PROD environment you want to run a t3.large instance.  These configurations can be defined here.  Environment supports the following sections:

* `dev` - Development Environment
* `test` - Test Environment
* `ppe` - Pre Production Environment
* `prod` - Production Environment

##### Mandatory environment variables
You must specify the following environment variables for Terragen to correctly generate your modules

* `region` - The AWS region you are deploying to
* `profile` - This is the profile you defined in your [Shared Credentials file above](#aws-credentials)
* `bucket` - [The name of the bucket you defined in above](#s3-bucket)

There is no requirement to use all sections, but you must specify at least one environment which you will point to in the `build` section below.  An example environment config, like the example we gave above might look like:

```yaml
dev:
  region: "us-east-1"
  profile: "dev_profile"
  bucket: "terragen_dev"
  intance_size: "t3.small"
prod:
  region: "us-east-1"
  profile: "prod_profile"
  bucket: "terragen_prod"
  intance_size: "t3.large"
```

#### 3. build 
`build` is the final section and it's a set of switches we can set to give us fine control over how the build in managed, each option explained below:

```yaml
cloud_provider: "AWSProvider"  # Provider used to create
environment: "prod"            # Deployment environment must be one of dev|test|ppe|prod
infra_shared: "create"         # Process shared infra, Must be one of create|destroy|pass
infra_app: "create"            # Process application infra, must be one of create|destroy|pass
terraform_mode: "apply"        # Must be one of plan|apply - Plan produces terraform plan only, apply will create or destroy infra
debug: True                    # Set to True to enable verbose debugging
```

This switches can be changed on the CLI making it easy to control the infra build in CI systems like Jenkins, CircleCI etc.  Which we'll see in the next section

## Creating Infrastructure
If we've completed our config correctly we should be able to run Terragen for our sample build to create our sample infrastructure

### Resolve Our Config
For our first run lets first check that Terragen can resolve the config we created above.  We need to tell Terragen where the config directory is located using the `--config-dir` switch or `-cd` for short.  We can also optionally supply the `--config-name` switch of `-cn` for short
```commandline
terragen --config-dir .\config --config-name config --cfg job --resolve
```

If successful the entire YAML of our configuration and base classes will be echod to the screen.  You can review this to see if it's what you expect.

### Running in Debug Mode
Next we are going to run with Debug set to True, this will generate all our Terraform modules with our configuration output as .tfvars file in the `outputs` directory, as follows:
```commandline
terragen -cd ./config build.debug=True
```

### Checking our generated Terraform modules in outputs dir
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
|------------------------vpc
```

### Applying our Infrastructure
If we're happy with the generated Terraform modules we can apply it, obviously with debug set to False, as follows:

```commandline
terragen -cd ./config build.debug=True
```

If everything is configured correctly you will have a new VPC called terragen-vpc and a EC2 instance called sandbox

## Destroying Infrastructure
If we've completed our config correctly we should be able to run Terragen for our sample build to create our sample infrastructure

To demonstrate how we can destroy only app level infrastructure rather than tearing everything down together, we will teardown app first then shared infra next.  In your own environment you might want to leave shared infra running.

```commandline
terragen -cd ./config infra_app=destroy
```

Once app infra is destroyed we can now destroy shared infra:
```commandline
terragen -cd ./config infra_shared=destroy
```

## Next Steps
If your comfortable with this getting started you should now be able to use Terragen to define your own infrastructure using your own Terraform Modules.

Review the [Terragen-Config](./terragen-config.md) section to get a deep dive into Configuration 