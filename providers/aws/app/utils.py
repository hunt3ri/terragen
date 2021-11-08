import toml
from omegaconf import ListConfig
from typing import Tuple


def to_toml(key: str, value):
    """Helper function returns the supplied key/value as valid toml"""
    if isinstance(value, str) and (value.startswith("data.")):
        return f"{key} = {value}"  # Lookups are variables and shouldn't be quoted
    elif isinstance(value, ListConfig):
        has_lookups, lookup_toml = lookup_to_toml(key, value)
        if has_lookups:
            return lookup_toml
        else:
            return toml.dumps({key: value}).strip()
    else:
        return toml.dumps({key: value}).strip()


def lookup_to_toml(key: str, lookup_list: ListConfig) -> Tuple[bool, str]:
    """By default toml will quote all items in the list, but if list item is a datasource it needs to remain unquoted"""
    lookup_str = f"{key} = ["
    lookup_cnt = 0
    for item in lookup_list:
        if item.startswith("data."):
            lookup_str = f"{lookup_str} {item},"
            lookup_cnt += 1
        else:
            lookup_str = f'{lookup_str} "{item}",'

    if lookup_cnt > 0:
        return True, f"{lookup_str}]"
    else:
        return False, ""
