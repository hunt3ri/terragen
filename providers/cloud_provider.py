from abc import abstractmethod
from omegaconf import DictConfig
import importlib
import logging

log = logging.getLogger(__name__)


class CloudProvider:
    # Extend functionality by registering new providers in format ClassName: module.path
    registered_providers = {
        "TerraGen": "providers.aws.terragen.terragen_provider"
    }
    name = "CloudProviderName"
    module = "CloudProviderModuleLocation"

    def build_provider(self, provider_name: str):
        """ Instantiate new instance of requested provider """
        try:
            log.info(f"Instantiating new provisioner: {provider_name}")
            self.name = provider_name
            self.module = self.registered_providers[provider_name]
        except KeyError:
            error = f"Provider {provider_name} not registered"
            log.critical(error)
            raise ValueError(error)

        my_module = importlib.import_module(self.module)

        provider = getattr(my_module, self.name)
        provider.name = provider_name
        provider.module = self.module
        return provider()

    @abstractmethod
    def create_shared_infra(self, infra_name: str, cfg: DictConfig):
        """ Providers can implement a method to create infra that is shared with multiple apps or infrastructure """
        raise NotImplementedError()

    @abstractmethod
    def destroy_shared_infra(self, cfg: DictConfig):
        """ Providers can implement a method to create infra that is shared with multiple apps or infrastructure """
        raise NotImplementedError()

    @abstractmethod
    def create_app_infra(self, cfg: DictConfig):
        """ Providers can implement a method to create infra for their application """
        raise NotImplementedError()

    @abstractmethod
    def destroy_app_infra(self, cfg: DictConfig):
        """ Providers can implement a method to destroy infra for their application """
        raise NotImplementedError()
