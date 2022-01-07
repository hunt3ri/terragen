# Terragen Configuration

## Terragen Config Structure
Terragen's config structure is flexible with the exception a few mandatory items.  As long as your config meets these criteria and your config correctly resolves then Terragen should parse it.  This page defines what these items are and shows how you can extend it for your own projects.

## Hydra
Terragen uses the Hydra Project to manage and parse configuration.  For a fuller understanding of configuring Terragen I recommend you take a look at the [Hydra Project Documentation here](https://hydra.cc/docs/intro).

## Bring Your Own Terraform Modules
Fundamentally Terragen is generating a [Terraform .tfvars](https://www.terraform.io/language/values/variables#variable-definitions-tfvars-files) file that will be injected into your module and then parsed by Terraform.  This means you can bring your own Terraform modules and use them with Terragen with almost zero changes.  Terragen will copy your Terraform Modules, and generate you a .tfvars file as per the configuration you specify in the Terragen config.  This page will explain how this can be controlled.

## Example Configs
If you haven't already please clone the example configs project so you can follow along with the examples below:

```commandline
git clone https://github.com/hunt3ri/terragen-example-configs.git
```

## Terragen Workspace 
If you've followed the Getting Started guide you should have your Terragen Workspace containing two directories:

* `config` containing the Terragen config which will be used to generate your tfvars files.
* `modules` containing the Terraform modules you want to apply.

We'll look at each in turn.

## config directory
The `config` directory must contain at least one config file, by default this is expected to be named `config.yaml`.  However, you can have multiple files here for different projects/pieces of infrastructure if needed.  You can run them by just referencing their names, eg:

```commandline
terragen --config-dir ./config --config-name my_web_app
```

It will also contain a set of sub-directories containing the specification of your config.  In our example you can see:

  * `apps` - App specific config files are here
  * `base` - These are base configs where we can "sub-class" in either apps or shared config files to override specific elements as needed
  * `shared` - Config for shared infrastructure like VPCs and Databases

Resulting in a structure as follows:

```
apps
base
shared
config.yaml
```

We'll dig into these files in more detail

### config.yaml defaults

The `defaults` section of config.yaml allows you to specify where the config file is located, and the namespace for the generated yaml.  As so:

```yaml
defaults:
  - aws/shared/vpcs@shared.vpc.simple_vpc: simple_vpc
```

Breaking down the structure we see the following 3 elements:
```yaml
- aws/shared/vpcs        @  shared.vpc.simple_vpc                         simple_vpc
  [path to config file]     [definition of namespace in generated yaml]   [file name for config]
```

So in our example configs you'll find the following file: `./aws/shared/vpcs/simple_vpc.yaml`

And when we resolve our config with the command `terragen -cd ./config -cn config --cfg job --resolve` We see Terragen has built our namespace exactly as we defined it:

```yaml
shared:
  vpc:
    simple_vpc:
      ...
```

### config namespaces
Terragen expects namespaces to be three levels deep, as follows:

  1. Level 1 - shared|app - whether the namespace refers to shared infrastructure or app specific infra
  2. Level 2 - infra type - the type of infra being generated, eg VPC, EC2, S3 etc
  3. Level 3 - infra name - your name for the infra being generated.  By convention, it is recommended to name your infra after the config file you're pointing to eg simple_vpc for simple_vpc.yaml

Follow this pattern and terraform should generate your terraform config correctly.

### environment and build
The environment and build elements of `config.yaml` are outlined in the Getting Started Guide

### infrastructure config files
Now that we understand how config.yaml controls where Terragen should look to find individual infrastructure  config files and how that namespace is rendered we can look at how to structure individual infrastructure config files.  We'll use our simple_vpc.yaml example, so lets open `./aws/shared/vpcs/simple_vpc.yaml`

You will see the following structure:

```yaml
defaults:
  - /aws/base/vpcs@: vpc_base

module_metadata:
  name        : "simple_vpc"
  state_file  : "shared/vpc/simple_vpc/terraform.tfstate"

config:
  vpc_name:             "hunter-labs-vpc"
  enable_dns_hostnames: true
```

#### defaults
Like `config.yaml` we have a defaults section.  This time we're specifying the base infrastructure file we're "sub-classing".  As before we can see the path to the file and it's name.  In the example above it's `./aws/base/vpcs/vpc_base.yaml` we'll look at base config files in just a moment.

#### module_metadata
This contains metadata about our config for example the name of the infrastructure we're generating, the name of the Terraform state file where state information is saved.  Again we'll dig into this in the base config section.

#### config
Finally we have the config section, this is the actual config we want to set for this piece of infra and is what will be generated in our tfvars file.  The values here should marry up with the variables you have set in your terraform module.

In our example the `enable_dns_hostnames` value must be a variable in our `modules/aws/vpc/variables.tf` file.  Indeed if we open the `variables.tf` file we will see:

```hcl
variable "enable_dns_hostnames" {
  description = "Set to true to enable DNS hostnames in the VPC, will generate public dns name for EC2 instance"
}
```

## Config Base Classes

Config base classes are where a lot of the power of Terragen lives.  Here we can define variables that must be overridden or defaults that are applied to every sub-classed config file.  For example, we can mandate a default instance size, a tagging scheme.  Allowing you to easily control and update dozens of pieces of infrastructure with one change.  Let's open `/aws/base/vpcs/vpc_base.yaml` and walk through it

```yaml
module_metadata:
  aws_service : "vpc"
  module_dir  : "modules/aws/vpc"
  name        : ???
  state_file  : ???

config:
  vpc_name:             ???
  cidr:                 "10.0.0.0/16"
  azs:                  ["us-east-1a", "us-east-1b"]
  public_subnets:       ["10.0.100.0/24", "10.0.200.0/24"]
  enable_dns_hostnames: false
  environment:          ${build.environment}

lookups:
```

You should note the same structure as the sub-class infrastructure `simple_vpc.yaml` we looked at above.  Clearly they must share the same structure for the sub-classing functionality to work.

#### module_metadata
As the name suggests this contains the metadata about your config and terraform modules.  It *MUST* contain the following elements

  * `aws_service` - The name of the aws_service we're using for this infrastructure
  * `module_dir` - The directory where Terragen can find the module to inject the config into
  * `name` - Name of the infrastructure you're generating.  You'll note the `???` value, this means the value must be overriden in all sub-classes
  * `statefile` - The path within your S3 bucket you want the statefile to be generated to.  Again the `???` indicates we expect this to be overridden in each infra sub-class file 

#### config
This is where you can specify the variables you want for your Terraform module.  Each value here should match the available variables in your terraform module `variables.tf` file, eg `modules/aws/vpc/variables.tf`

#### lookups
The final section is lookups.  This is an optional section and is only required if your module needs to lookup a value from another statefile, using a [Terraform data source](https://www.terraform.io/language/data-sources) 

The lookups section is how you can notify Terragen of the requirement to inject your config into the `data.tf` file in your terraform module.  

If you open `./aws/apps/sandbox/sandbox.yaml` You'll see the following in the lookups section:

```yaml
lookups:
  vpc_statefile       : ${shared.vpc.simple_vpc.module_metadata.state_file}
```

Here we're telling Terragen to lookup the value that is represented in the namespace `shared.vpc.simple_vpc.module_metadata.state_file` and inject it into the modules `data.tf` file.

If we open up the matching `data.tf` file at `modules/aws/ec2/data.tf` You will see the following:

```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket  = "{{ bucket }}"
    key     = "{{ lookups['vpc_statefile'] }}"
    profile = "{{ profile }}"
    region  = "{{ region }}"
  }
}
```
This is a Jinja template and it is how Terragen injects your specified config.  You'll see more on this in the modules section below.

This means we can create dynamic data files based on your config and the location of your terraform statefile as defined in your config :)

This is a little complex to get your head around but hopefully the examples make it clear how to achieve this

## Terragen Config Syntax

Config files in Terragen should all be valid YAML.  Beyond that there are a couple of special values you can use to flag a value is mandatory in a base config file, and to lookup a value from a different namespace.  We'll look at both here.

### Mandatory Value
Mandatory values are a powerful feature of Terragen and can enable you to enforce, for example, an AWS tagging scheme by enforcing sub-classed config files have to enter a value for all tags.  You can see examples in the `/aws/base/vpcs/vpc_base.yaml` file.  Picking one example:

```yaml
config:
  vpc_name:             ???
  cidr:                 "10.0.0.0/16"
```

Here we have specified that sub-class configs must supply a name for the vpc.  If they don't specify a name in sub-class infrastructure file the following error will be generated when you run Terragen.

First we run Terragen

```commandline
terragen -cd ./config -cn config
```

Now we see the error.  Meaning Terragen should make it easy for users to understand when they need to supply mandatory values:

```commandline
[2022-01-07 00:06:29,338][terragen.cli][INFO] - Validating Config
[2022-01-07 00:06:29,340][terragen.cli][ERROR] - Config Error: Missing mandatory value: name
    full_key: shared.vpc.simple_vpc.module_metadata.name
    object_type=dict
```

### Lookup Value
The last special command we'll look at is lookups.  It is often useful to lookup values from other config files to inject into your configuration.  A simple example would be the requirement to inject the environment name into a tag or instance name, eg dev, ppe, prd.  So an instance might be named webappdev.

If we open up the `/aws/base/vpcs/vpc_base.yaml` file again we can see the following line:

```yaml
  environment:          ${build.environment}
```

Here we are telling Terragen to lookup the value from the build.environment variable that is defined in the `config.yaml` file.  Here

```yaml
build:
  cloud_provider: "AWSProvider"
  environment: "prod"  
```

This means the value will dynamically change when we build prd, test, dev environments.

### Further reading on config
You can find more info on Lookups, Mandatory values and more in both the [Hydra documentation](https://hydra.cc/docs/intro/) and [OmegaConf project](https://omegaconf.readthedocs.io/) (which Hydra leverages)

## modules directory
We now come to the modules directory.  Which is where all your Terraform modules reside.  We expect you to be familiar with defining Terraform modules but do check the excellent docs at Hashicorp to find out more.

Terragen's aim is to allow you to use your existing Terraform modules with almost no changes.  So please import them into the modules directory.

### Defining Your Terraform Modules
As stated earlier Terragen basically generates a .tfvars file that will be applied along with your modules.  So for the dynamic values of your infrastructure, such as name, instance_size tags and so on.  These should all be controlled by variables.  If you look at the modules directory in our example.  You should see that the `variables.tf` file matches up with the .tfvars file that Terragen generates.

We can check this by running Terragen and inspecting the .tfvars file that Terragen generates.  We first run Terragen:

```commandline
terragen -cd ./config -cn config
```

Now if we open the `outputs` directory and navigate to `outputs/DATE/TIME/AWSProvider/prod/vpc/simple_vpc/simple_vpc.tfvars` we can see Terragen has generated us the .tfvars file as specified by our config.

```hcl
vpc_name = "hunter-labs-vpc"
cidr = "10.0.0.0/16"
azs = [ "us-east-1a", "us-east-1b",]
public_subnets = [ "10.0.100.0/24", "10.0.200.0/24",]
enable_dns_hostnames = true
environment = "prod"
```

### Your Data Module
The ONLY file you need to modify is your data.tf file if your module needs to lookup a value from a different statefile.  This is typically something in your shared config, like a VPC name, RDS id etc.

If we look at our example project and open the `data.tf` file at `modules/aws/ec2/data.tf` You will see the following:

```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket  = "{{ bucket }}"
    key     = "{{ lookups['vpc_statefile'] }}"
    profile = "{{ profile }}"
    region  = "{{ region }}"
  }
}
```

This is a Jinja template and Terragen will inject in the appropriate config to allow Terraform to access the correct statefile.  We can see this in action again by running terragen

```commandline
terragen -cd ./config -cn config
```

If we again navigate to our `outputs` directory at `outputs/DATE/TIME/AWSProvider/prod/ec2/sandbox/data.tf` we can see that the template in our modules directory has now been correctly populated.

```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket  = "hunter-ops-tfstate"
    key     = "shared/vpc/simple_vpc/terraform.tfstate"
    profile = "hunter_ops_prod"
    region  = "us-east-1"
  }
}
```

Again this may seem a bit complex, but hopefully the example project allows you to play around to understand this functionality more fully.