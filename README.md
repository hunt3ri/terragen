# terragen
This project is an opinionated framework for generating and managing terraform modules and resources for sophisticated Cloud Architectures

Config is read from the local ```config``` directory.  [Config is controlled by the hydra framework, check the docs for examples](https://hydra.cc/docs/intro/)


## Running
Supply the generate.py app the name of the config file
```commandline
python .\terragen.py --config-name sandbox
```

## Overriding values on command line
Any config value can be overridden on the command line using dot notation, eg:
```commandline
python .\terragen.py build.environment=test
```

## Debugging
Run generator with cfg and resolve flags to output interpolations
```commandline
python .\terragen.py --cfg job --resolve
```
Alternatively you can print to screen, file using following
```python
print(OmegaConf.to_yaml(cfg, resolve=True))
```

You can enable verbose debug logging by passing the following:
```commandline
python .\terragen.py hydra.verbose=true
```

## Dev Commands
Linting:
```flake8```

Formatting:
```black .```
