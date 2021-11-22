# terragen
Terragen is a framework for generating and automatically applying Terraform modules to simplify the management of sophisticated Cloud Architectures

Config is read from the local ```config``` directory.  [Config is controlled by the hydra framework, check the docs for examples](https://hydra.cc/docs/intro/)

## Key Features
TODO

## Installing
Terragen can be installed via pip:

```commandline
pip install terragen
```

## Documentation
TODO

## Quick Start
Terragen expects two directories of configuration to be created. modules containing all terraform modules you want to configure. config containing the configuration for each module you want to deploy.  A sample directory structure shown below:
```commandline
--config
----__init__.py
----config.yaml
--modules
----aws
--------ec2
------------main.tf
```

## Running
Terragen looks for a default config.yaml file in config directory, if that is present you can just run terragen
```commandline
terragen
```
You can also create specfic config files for certain applications, eg
```commandline
terragen --config-name sandbox
```

## Overriding values on command line
Any config value can be overridden on the command line using dot notation, eg:
```commandline
terragen build.environment=test
```

## Debugging
Run Terragen with cfg and resolve flags to output interpolations
```commandline
terragen --cfg job --resolve
```

You can enable verbose debug logging by passing the following:
```commandline
terragen hydra.verbose=true
```
