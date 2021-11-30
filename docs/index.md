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

## Getting Started

### Installing
Terragen is installed via pip, as follows:

```commandline
pip install terragen
```

### Creating your first infrastructure

Terragen expects two directories to be present to successfully run.  Directory layout should look like this:

```commandline
|-config
|----config.yaml
|-modules
```
* config - Containing the Terragen configuration
* modules - Containing the Terraform modules you want Terragen to apply

Examples of which can be found in our [github repo](https://github.com/hunt3ri/terragen)