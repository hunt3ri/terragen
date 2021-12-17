from abc import abstractmethod
from omegaconf import DictConfig
import attr
import importlib
import logging

log = logging.getLogger(__name__)

# A list of implemented providers.  Could be made configurable if required
available_providers = {
    "AWSProvider": "providers.aws.aws_provider"
}


@attr.s
class BuildProperties:
    cloud_provider: str = attr.ib()
    environment: str = attr.ib()
    infra_shared: str = attr.ib()
    infra_app: str = attr.ib()
    terraform_mode: str = attr.ib()
    debug_mode: bool = attr.ib(default=False)

    @cloud_provider.validator
    def is_valid_cloud_provider(self, attribute, value):
        if value not in ["AWSProvider"]:
            raise ValueError("build.cloud_provider must be AWSProvider")

    @environment.validator
    def is_valid_environment(self, attribute, value):
        if value not in ["dev", "test", "ppe", "prod"]:
            raise ValueError("build.environment must be one of dev|test|ppe|prod")

    @infra_shared.validator
    @infra_app.validator
    def is_valid_infra_mode(self, attribute, value):
        if value not in ["crate", "destroy", "pass"]:
            raise ValueError("build.infra_app and build.infra_shared  must be one of create|destroy|pass")

    @cloud_provider.validator
    def is_valid_terraform_mode(self, attribute, value):
        if value not in ["plan", "apply"]:
            raise ValueError("build.terraform_mode must be one of plan|apply")

    @classmethod
    def from_build_config(cls, build_config: DictConfig):

        return cls(
            cloud_provider=build_config.cloud_provider,
            environment=build_config.environment,
            infra_shared=build_config.infra_shared,
            infra_app=build_config.infra_app,
            terraform_mode=build_config.terraform_mode,
            debug_mode=build_config.debug
        )



@attr.s
class CloudProvider:

    debug_mode: bool = attr.ib()
    environment: str = attr.ib()
    provider_name: str = attr.ib()
    terraform_mode: str = attr.ib()
    #provider_properties: DictConfig = attr.ib()

    @staticmethod
    def from_build_config(provider_name: str, build_config: DictConfig):
        log.info(f"Instantiating Cloud Provider: {provider_name}")
        provider_location = available_providers[provider_name]

        # Dynamically load the CloudProvider module by name
        cloud_provider = getattr(importlib.import_module(provider_location), provider_name)

        teraform_mode = build_config.terraform_mode.lower()
        if teraform_mode not in ["plan", "apply"]:
            raise ValueError("build.terraform_mode, must be one of plan or apply")

        return cloud_provider(
            provider_name=provider_name,
            environment=build_config.environment,
            debug_mode=build_config.debug,
            terrform_mode=teraform_mode
        )

    @abstractmethod
    def create_infra(self, module_config: DictConfig, environment_config: DictConfig):
        """Providers must implement a method for creating all infrastructure"""
        raise NotImplementedError()

    @abstractmethod
    def destroy_infra(self, module_config: DictConfig, environment_config: DictConfig):
        """Providers must implement a method for destroying all infrastructure"""
        raise NotImplementedError()
