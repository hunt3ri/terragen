import pytest

from terragen.providers.aws.app.utils import to_toml, get_env_var

from dataclasses import dataclass
from omegaconf import OmegaConf


@dataclass
class TerraformTags:
    name: str = "TestInstance"


@dataclass
class EnvironmentVars:
    api_key: str = "skhfks"
    password: str = "dfjdkfj"


@dataclass
class MockEC2Config:
    ami: str = "ami-06310010cdfb6a743"
    instance_type: str = "t3a.small"
    subnet_id: str = "data.terraform_remote_state.simple_vpc.outputs.public_subnets[0]"
    associate_public_ip_address: bool = True
    tags: TerraformTags = TerraformTags()
    env_vars: EnvironmentVars = EnvironmentVars()
    iam_policy: str = '<<EOT\n{\n Version": "2012-10-17",\nEoT'


class TestUtils:
    @pytest.fixture()
    def mock_ec2_config(self) -> MockEC2Config:
        return OmegaConf.structured(MockEC2Config)

    def test_to_toml_happy_path(self, mock_ec2_config):
        assert to_toml("ami", mock_ec2_config.ami) == f'ami = "{mock_ec2_config.ami}"'

    def test_to_toml_handles_lookups(self, mock_ec2_config):
        lookup_value = to_toml("subnet_id", mock_ec2_config.subnet_id)
        assert lookup_value == "subnet_id = data.terraform_remote_state.simple_vpc.outputs.public_subnets[0]"

    def test_to_toml_handles_dicts(self, mock_ec2_config):
        lookup_value = to_toml("env_vars", mock_ec2_config.env_vars)
        assert lookup_value == 'env_vars = {\n    api_key = "skhfks"\n    password = "dfjdkfj"\n }'

    def test_get_env_var_raise_error_if_env_var_not_set(self):
        with pytest.raises(ValueError):
            get_env_var("env.MY_TEST")

    def test_iam_policy_parsed_correctly(self, mock_ec2_config):
        # IAM Policies need to start with <<EOT to be parsed correctly
        lookup_value = to_toml("iam_policy", mock_ec2_config.iam_policy)
        assert lookup_value == 'iam_policy = <<EOT\n{\n Version": "2012-10-17",\nEoT'
