# terragen
Terragen is a framework for generating and automatically applying Terraform modules to simplify the management of sophisticated Cloud Architectures

Config is read from the local ```config``` directory.  [Config is controlled by the hydra framework, check the docs for examples](https://hydra.cc/docs/intro/)


## Running
Supply Terragen the name of the config file
```commandline
python .\terragen.py --config-name sandbox
```

## Overriding values on command line
Any config value can be overridden on the command line using dot notation, eg:
```commandline
python .\terragen.py build.environment=test
```

## Debugging
Run Terragen with cfg and resolve flags to output interpolations
```commandline
python .\terragen.py --cfg job --resolve
```

You can enable verbose debug logging by passing the following:
```commandline
python .\terragen.py hydra.verbose=true
```
