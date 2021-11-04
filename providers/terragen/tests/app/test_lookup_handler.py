import pytest

from dataclasses import dataclass, field
from omegaconf import OmegaConf
from providers.terragen.app.lookup_handler import LookupHandler
from typing import List


@dataclass
class ModuleConfig:
    ami: str = "ami-06310010cdfb6a743"
    instance_type: str = "t3a.small"
    subnet_id: str = "lookup: ${shared.vpc.simple_vpc.outputs.public_subnet_ids.lookup}[0]"
    associate_public_ip_address: bool = True
    vpc_security_group_ids: List[str] = field(default_factory=lambda: ['lookup: ${app.security_groups.local_access.outputs.security_group_id.lookup}'])


class TestLookupHandler:

    @pytest.fixture()
    def module_config(self):
        return OmegaConf.structured(ModuleConfig)

    @pytest.fixture()
    def lookup_handler(self, module_config):
        return LookupHandler.from_module_config("test_module", module_config)

    def test_get_lookup_values(self, lookup_handler):
        datablock_key, datablock_lookup = lookup_handler.get_lookup_values("lookup: shared.vpc.simple_vpc.outputs.vpc_id")
        assert datablock_key == "shared/vpc/simple_vpc"
        assert datablock_lookup == "outputs.vpc_id"

    def test_get_lookup_values_raises_error_for_missing_outputs(self, lookup_handler):
        with pytest.raises(ValueError):
            lookup_handler.get_lookup_values("lookup: shared.vpc.simple_vpc")