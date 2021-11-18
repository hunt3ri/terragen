import pytest

from providers.aws.app.utils import to_toml

from dataclasses import dataclass
from omegaconf import OmegaConf


@dataclass
class TerraformTags:
    name: str = "TestInstance"


@dataclass
class MockEC2Config:
    ami: str = "ami-06310010cdfb6a743"
    instance_type: str = "t3a.small"
    subnet_id: str = "data.terraform_remote_state.simple_vpc.outputs.public_subnets[0]"
    associate_public_ip_address: bool = True
    tags: TerraformTags = TerraformTags()


class TestUtils:
    @pytest.fixture()
    def mock_ec2_config(self) -> MockEC2Config:
        return OmegaConf.structured(MockEC2Config)

    def test_to_toml_happy_path(self, mock_ec2_config):
        assert to_toml("ami", mock_ec2_config.ami) == f'ami = "{mock_ec2_config.ami}"'

    def test_to_toml_handles_lookups(self, mock_ec2_config):
        lookup_value = to_toml("subnet_id", mock_ec2_config.subnet_id)
        assert lookup_value == "subnet_id = data.terraform_remote_state.simple_vpc.outputs.public_subnets[0]"
