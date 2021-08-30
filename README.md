# py-tfvars
This project generates and applies terraform tfvars file.  Config is specified in the config directory.  [Config is controlled by the hydra framework, check the docs for examples](https://hydra.cc/docs/intro/)


## Running
Supply the generate.py app the name of the config file
```commandline
python .\generate.py --config-name sandbox
```

## Overriding values on command line
Any config value can be overridden on the command line using dot notation, eg:
```commandline
python .\generate.py build.environment=prod vpc.vpc_name="HELLO_WORLD"
```

## Debugging
Run generator with cfg and resolve flags to output interpolations
```commandline
python .\generate.py --cfg job --resolve
```
Alternatively you can print to screen, file using following
```python
print(OmegaConf.to_yaml(cfg, resolve=True))
```