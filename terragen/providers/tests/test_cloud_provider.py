import pytest
from terragen.providers.cloud_provider import BuildConfig
from dataclasses import dataclass
from omegaconf import OmegaConf


@dataclass
class MockBuildConfig:
    """Models a valid build config as would be set in main config.yaml"""

    cloud_provider: str = "AWSProvider"
    environment: str = "prod"
    infra_shared: str = "create"
    infra_app: str = "create"
    terraform_mode: str = "apply"
    debug: bool = False


class TestUtils:
    @pytest.fixture()
    def mock_build_config(self) -> MockBuildConfig:
        return OmegaConf.structured(MockBuildConfig)

    def test_build_properties_invalid_cloud_provider(self, mock_build_config):
        with pytest.raises(ValueError):
            mock_build_config.cloud_provider = "Azure"
            BuildConfig.from_build_config_yaml(mock_build_config)

    def test_build_properties_invalid_environment(self, mock_build_config):
        with pytest.raises(ValueError):
            mock_build_config.environment = "invalid"
            BuildConfig.from_build_config_yaml(mock_build_config)

    def test_build_properties_invalid_infra_shared(self, mock_build_config):
        with pytest.raises(ValueError):
            mock_build_config.infra_shared = "invalid"
            BuildConfig.from_build_config_yaml(mock_build_config)

    def test_build_properties_invalid_infra_app(self, mock_build_config):
        with pytest.raises(ValueError):
            mock_build_config.infra_app = "invalid"
            BuildConfig.from_build_config_yaml(mock_build_config)

    def test_build_properties_invalid_terraform_mdoe(self, mock_build_config):
        with pytest.raises(ValueError):
            mock_build_config.terraform_mode = "invalid"
            BuildConfig.from_build_config_yaml(mock_build_config)
