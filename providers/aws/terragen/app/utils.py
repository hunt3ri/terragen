import toml


def to_toml(key, value):
    """ Helper function returns the supplied key/value as valid toml """
    return toml.dumps({key: value}).rstrip()
