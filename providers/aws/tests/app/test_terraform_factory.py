import pytest

from dataclasses import dataclass, field
from omegaconf import OmegaConf
from providers.aws.app.terraform_factory import TerraformFactory
from typing import List

@dataclass
class RootBlockDevice:
    encrypted: bool = True
    volume_size: int = 8
    volume_type: str = "gp3"

@dataclass
class MockEC2Config:
    ami: str = "ami-06310010cdfb6a743"
    instance_type: str = "t3a.small"
    subnet_id: str = "lookup: shared.vpc.simple_vpc.outputs.public_subnet_ids[0]"
    associate_public_ip_address: bool = True
    vpc_security_group_ids: List[str] = field(
        default_factory=lambda: ["lookup: app.security_groups.local_access.outputs.security_group_id"]
    )
    root_block_device: RootBlockDevice = RootBlockDevice()


class TestTerraformFactory:

    @pytest.fixture()
    def mock_ec2_config(self) -> MockEC2Config:
        return OmegaConf.structured(MockEC2Config)

    @pytest.fixture()
    def mock_terraform_factory(self, mock_ec2_config: MockEC2Config) -> TerraformFactory:
        tf_factory = TerraformFactory.from_test_class()
        tf_factory.module_config = mock_ec2_config
        return tf_factory

    def test_parse_config_for_dictionaries(self, mock_terraform_factory):
        iain = mock_terraform_factory.dictconfig_handler(mock_terraform_factory.module_config.root_block_device)
