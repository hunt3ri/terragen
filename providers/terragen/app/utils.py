import toml
from omegaconf import ListConfig


def to_toml(key: str, value):
    """ Helper function returns the supplied key/value as valid toml """
    if isinstance(value, str) and (value.startswith("data.")):
        return f"{key} = {value}"  # Lookups are variables and shouldn't be quoted
    elif isinstance(value, ListConfig):
        """ By default lists will quote the datasource lookups, so we need to ensure they remain unquoted """
        lookup_str = f"{key} = ["
        lookup_cnt = 0
        for item in value:
            if item.startswith("data."):
                lookup_str = f'{lookup_str} {item},'
                lookup_cnt += 1
            else:
                lookup_str = f'{lookup_str} "{item}",'

        if lookup_cnt > 0:
            return f"{lookup_str}]"
        else:
            return toml.dumps({key: value}).strip()
    else:
        return toml.dumps({key: value}).strip()
