# Welcome to Terragen

Terragen is a framework for generating and automatically applying Terraform modules to simplify the management of sophisticated Cloud Architectures

## Key Features
 * Simplify the creation and destruction of infra across multiple accounts and regions, using one command
 * Fine grained CLI control, all config elements can be overridden on the CLI
 * View generated Terraform files before they are applied.  Each run creates a timestamped output directory
 * Control common and app specific infra separately.  Infra that is shared, eg VPCs, Databases can be controlled separately but still referenced by app specific infra
 * Create base config files you can "sub-class" for specific implementations, allows you to enforce config patterns across your estate
 * Boiler plate Terraform files, like config, tfvars automatically generated
 * Variable interpolation.  Lookup values from other config files.

### Pre-requisites
* Terraform - You must have Terraform installed locally to allow Terragen to run the Terraform CLI.  [See Installing Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## Getting Started
You can find getting started guides for each cloud provider here:

* [AWS](./getting-started-aws.md)

## Next Steps
Once comfortable with the Getting-Started guide, get a deep dive into Terragen Configuration here:

* [Cloud Configuration with Terragen](./terragen-config.md)

## Issues and Questions
Please raise any issues or questions you have on the project Github page:

* [Terragen Github](https://github.com/hunt3ri/terragen)