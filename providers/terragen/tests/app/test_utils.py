import pytest

from providers.terragen.app.utils import to_toml

from dataclasses import dataclass, field
from omegaconf import OmegaConf
from providers.terragen.app.lookup_handler import LookupHandler
from typing import List


@dataclass
class MockEC2Config:
    """ This mock represents an object that has already been parsed by the lookup handler"""
    ami: str = "ami-06310010cdfb6a743"
    instance_type: str = "t3a.small"
    subnet_id: str = "data.terraform_remote_state.simple_vpc.outputs.public_subnets[0]"
    associate_public_ip_address: bool = True
    vpc_security_group_ids: List[str] = field(default_factory=lambda: ['data.terraform_remote_state.local_access.outputs.security_group_id'])


class TestUtils:

    @pytest.fixture()
    def mock_ec2_config(self) -> MockEC2Config:
        return OmegaConf.structured(MockEC2Config)

    def test_to_toml_happy_path(self, mock_ec2_config):
        assert to_toml("ami", mock_ec2_config.ami) == f'ami = "{mock_ec2_config.ami}"'

    def test_to_toml_handles_lookups(self, mock_ec2_config):
        lookup_value = to_toml("subnet_id", mock_ec2_config.subnet_id)
        assert lookup_value == "subnet_id = data.terraform_remote_state.simple_vpc.outputs.public_subnets[0]"

    def test_to_toml_handles_lists_with_lookups(self, mock_ec2_config):
        lookup_value = to_toml("vpc_security_group_ids", mock_ec2_config.vpc_security_group_ids)
        assert lookup_value == 'vpc_security_group_ids = [ data.terraform_remote_state.local_access.outputs.security_group_id,]'
