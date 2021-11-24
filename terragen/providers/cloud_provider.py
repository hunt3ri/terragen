from abc import abstractmethod
from omegaconf import DictConfig
import attr
import importlib
import logging

log = logging.getLogger(__name__)


@attr.s
class CloudProvider:

    debug_mode: bool = attr.ib()
    environment: str = attr.ib()
    provider_name: str = attr.ib()
    provider_properties: DictConfig = attr.ib()

    @staticmethod
    def from_build_config(provider_name: str, build_config: DictConfig):
        log.info(f"Instantiating Cloud Provider: {provider_name}")
        provider_config = build_config.registered_providers[provider_name]

        # Dynamically load the CloudProvider module by name
        cloud_provider = getattr(importlib.import_module(provider_config.module_location), provider_name)

        return cloud_provider(
            provider_name=provider_name,
            environment=build_config.environment,
            provider_properties=provider_config.properties,
            debug_mode=build_config.debug,
        )

    @abstractmethod
    def create_infra(self, cfg: DictConfig):
        """Providers must implement a method for creating all infrastructure"""
        raise NotImplementedError()

    @abstractmethod
    def destroy_infra(self, cfg: DictConfig):
        """Providers must implement a method for destroying all infrastructure"""
        raise NotImplementedError()
