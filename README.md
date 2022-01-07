# terragen
Terragen is a framework for generating and automatically applying Terraform modules to simplify the management of sophisticated Cloud Architectures

## Key Features
 * Simplify the creation and destruction of infra across multiple accounts and regions, using one command
 * Fine grained CLI control, all config elements can be overridden on the CLI
 * View generated Terraform files before they are applied.  Each run creates a timestamped output directory
 * Control common and app specific infra separately.  Infra that is shared, eg VPCs, Databases can be controlled separately but still referenced by app specific infra
 * Create base config files you can "sub-class" for specific implementations, allows you to enforce config patterns across your estate
 * Boiler plate Terraform files, like config, tfvars automatically generated
 * Variable interpolation.  You can lookup values from other config files.

## Installing
Terragen can be installed via pip:

```commandline
pip install terragen
```

## ReadTheDocs
[Full details on configuring and running Terragen on ReadTheDocs](https://terragen.readthedocs.io/en/latest/)

## Terragen Workspace
Terragen expects to be run in its own workspace containing its configuration and the Terraform modules you want to configure and apply.

* [Demo Workspace is available here](https://github.com/hunt3ri/terragen-example-configs)

## Demo Commands
Once configured as defined in docs, Terragen is very powerful.  Below we demonstrate some commands

### Applying a Named Config
Terragen lets you define multiple apps and configs, just apply them by name
```commandline
terragen --config-dir ./config --config-name sandbox
```

### Specifying the environment we want to deploy to
Terragen lets you create the same infrastructure across multiple accounts by supplying the environment you want to deploy to
```commandline
terragen --config-dir ./config build.environment=test
```

## Debugging
Validate and resolve your config before you run it.
```commandline
terragen -cd ./config --cfg job --resolve
```
### Verbose debugging
You can enable verbose debug logging by passing the following:
```commandline
terragen -cd ./config hydra.verbose=true
```
