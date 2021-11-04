import toml


def to_toml(key: str, value):
    """ Helper function returns the supplied key/value as valid toml """
    if isinstance(value, str) and (value.startswith("data.")):
        return f"{key} = {value}"  # Lookups are variables and shouldn't be quoted
    else:
        return toml.dumps({key: value}).strip()


def get_lookup_values(lookup: str):
    clean_lookup = lookup.replace("lookup:", "").strip()
    lookup_array = clean_lookup.split('.outputs')

    if len(lookup_array) != 2:
        raise ValueError(f"Supplied lookup {lookup} does not contain .outputs")

    datablock_key = lookup_array[0].replace(".", "/")
    datablock_lookup = f"outputs{lookup_array[1]}"

    return datablock_key, datablock_lookup

