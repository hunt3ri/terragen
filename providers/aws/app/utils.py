import toml


def to_toml(key: str, value):
    """Helper function returns the supplied key/value as valid toml"""
    if isinstance(value, str) and (value.startswith("data.")):
        return f"{key} = {value}"  # Lookups are variables and shouldn't be quoted
    else:
        return toml.dumps({key: value}).strip()
