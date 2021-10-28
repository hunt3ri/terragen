import pytest
from providers.terragen.app.utils import get_lookup_values


def test_get_lookup_values():
    datablock_key, datablock_lookup = get_lookup_values("lookup: shared.vpc.simple_vpc.outputs.vpc_id")
    assert datablock_key == "shared/vpc/simple_vpc"
    assert datablock_lookup == "outputs.vpc_id"


def test_get_lookup_values_raises_error_for_missing_outputs():
    with pytest.raises(ValueError):
        get_lookup_values("lookup: shared.vpc.simple_vpc")
