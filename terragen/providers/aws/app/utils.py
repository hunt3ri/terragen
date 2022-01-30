import logging
import os
import toml

from omegaconf import DictConfig


log = logging.getLogger(__name__)


def to_toml(key: str, value):
    """Helper function returns the supplied key/value as valid toml"""
    if isinstance(value, str) and (value.startswith("data.")):
        return f"{key} = {get_env_var(value)}"  # Lookups are variables and shouldn't be quoted
    elif isinstance(value, DictConfig):
        return to_hcl_map(key, value)
    else:
        return toml.dumps({key: value}).strip()


def to_hcl_map(key: str, config: DictConfig):
    """ Helper to return a dictionary of config into a HCL map """
    hcl_map = f"{key} = {{\n"
    for key, value in config.items():
        hcl_map = f'{hcl_map}    {key} = "{get_env_var(value)}"\n'

    return f"{hcl_map} }}"


def get_env_var(value: str):
    """ Check if value has an env var set and if so attempts to look it up """
    if "env." not in value:
        return value

    env_var_key = value.split(".")[-1]
    env_var_value = os.getenv(env_var_key, "NOT_SET")

    if env_var_value == "NOT_SET":
        error_message = f"ERROR: Environment Variable {env_var_key} not set "
        log.error(error_message)
        raise ValueError(error_message)

    return env_var_value
