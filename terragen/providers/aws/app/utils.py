import toml
import os
from pathlib import Path
import logging

log = logging.getLogger(__name__)


def to_toml(key: str, value):
    """Helper function returns the supplied key/value as valid toml"""
    if isinstance(value, str) and (value.startswith("data.")):
        return f"{key} = {value}"  # Lookups are variables and shouldn't be quoted
    else:
        return toml.dumps({key: value}).strip()


def locate_module() -> str:
    """ Locate where the modules directory is from current working dir """
    full_path = os.getcwd()
    log.debug(f"Full Path: {full_path}")
    levels = 1
    parent_dirs = "../.."

    while levels <= 5:
        levels += 1  # Modules must be a minimum of 3 levels up
        parent_dirs = f"../{parent_dirs}"
        module_path = str(Path(full_path).parents[levels])
        subdirs = [f.path for f in os.scandir(module_path) if f.is_dir()]
        for dir in subdirs:
            if "modules" in dir:
                return parent_dirs
