import pytest

from dataclasses import dataclass, field
from omegaconf import OmegaConf
from providers.terragen.app.lookup_handler import LookupHandler
from typing import List


@dataclass
class MockEC2Config:
    ami: str = "ami-06310010cdfb6a743"
    instance_type: str = "t3a.small"
    subnet_id: str = "lookup: shared.vpc.simple_vpc.outputs.public_subnet_ids[0]"
    associate_public_ip_address: bool = True
    vpc_security_group_ids: List[str] = field(default_factory=lambda: ['lookup: app.security_groups.local_access.outputs.security_group_id'])


class TestLookupHandler:

    @pytest.fixture()
    def mock_ec2_config(self):
        return OmegaConf.structured(MockEC2Config)

    @pytest.fixture()
    def lookup_handler(self, mock_ec2_config):
        return LookupHandler.from_module_config("test_module", mock_ec2_config)

    def test_set_lookup_values_ignores_bools(self, lookup_handler):
        lookup_handler.set_lookup_values("associate_public_ip_address", MockEC2Config.associate_public_ip_address)
        assert len(lookup_handler.datablock_keys) == 0

    def test_set_lookup_values_ignores_non_lookup_strings(self, lookup_handler):
        lookup_handler.set_lookup_values("instance_type", MockEC2Config.instance_type)
        assert len(lookup_handler.datablock_keys) == 0

    def test_set_lookup_values_parses_lookup_string_correctly(self, lookup_handler):
        lookup_handler.set_lookup_values("subnet_id", MockEC2Config.subnet_id)
        assert lookup_handler.datablock_keys[0] == 'shared/vpc/simple_vpc'
        assert lookup_handler.module_config.subnet_id == 'data.terraform_remote_state.test_module.outputs.public_subnet_ids[0]'

    def test_set_lookup_values_parses_lookup_list(self, lookup_handler):
        # Arrange
        sg_ids = lookup_handler.module_config.vpc_security_group_ids
        lookup_handler.datablock_keys = []

        # Act
        lookup_handler.set_lookup_values("vpc_security_group_ids", sg_ids)
        assert lookup_handler.datablock_keys[0] == 'app/security_groups/local_access'
        assert lookup_handler.module_config.vpc_security_group_ids[0] == 'data.terraform_remote_state.test_module.outputs.security_group_id'

    def test_get_lookup_values_raises_error_for_missing_outputs(self, lookup_handler):
        with pytest.raises(ValueError):
            lookup_handler.get_lookup_values("lookup: shared.vpc.simple_vpc")