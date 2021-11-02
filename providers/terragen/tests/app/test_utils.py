import pytest
from providers.terragen.app.utils import get_lookup_values, to_toml


def test_get_lookup_values():
    datablock_key, datablock_lookup = get_lookup_values("lookup: shared.vpc.simple_vpc.outputs.vpc_id")
    assert datablock_key == "shared/vpc/simple_vpc"
    assert datablock_lookup == "outputs.vpc_id"


def test_get_lookup_values_raises_error_for_missing_outputs():
    with pytest.raises(ValueError):
        get_lookup_values("lookup: shared.vpc.simple_vpc")


def test_to_toml_happy_path():
    assert to_toml("happy", "path") == 'happy = "path"'


def test_to_toml_handles_lookups():
    lookup_value = to_toml("lookup", "data.terraform_remote_state.local_access.outputs.vpc_id")
    assert lookup_value == "lookup = data.terraform_remote_state.local_access.outputs.vpc_id"
