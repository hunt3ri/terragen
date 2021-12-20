# terragen
Terragen is a framework for generating and automatically applying Terraform modules to simplify the management of sophisticated Cloud Architectures

Config is read from the local ```config``` directory.  [Config is controlled by the hydra framework, check the docs for examples](https://hydra.cc/docs/intro/)

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
[You can find docs on configuring and running Terragen on ReadTheDocs](https://terragen.readthedocs.io/en/latest/)

## Demo commands 
We demonstrate the power and flexibility of Terragen here

## Running
Terragen looks for a default config.yaml file in config directory.  You must specify location of config directory using `--config-dir` or `-cd`, for example:
```commandline
terragen --config-dir ./config
```
You can also create specfic config files for certain applications, eg
```commandline
terragen -cd ./config --config-name sandbox
```

## Overriding values on command line
Any config value can be overridden on the command line using dot notation, eg:
```commandline
terragen --config-dir ./config build.environment=test
```

## Debugging
Run Terragen with cfg and resolve flags to output interpolations
```commandline
terragen -cd ./config --cfg job --resolve
```

You can enable verbose debug logging by passing the following:
```commandline
terragen -cd ./config hydra.verbose=true
```
