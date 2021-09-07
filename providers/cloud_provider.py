from abc import abstractmethod
from omegaconf import DictConfig
import importlib


class CloudProvider:
    # Extend functionality by registering new providers in format ClassName: module.path
    registered_providers = {
        "AWSTerraformProvider": "providers.aws.terraform.terraform_provider"
    }
    name = "CloudProviderName"
    module = "CloudProviderModuleLocation"

    def build_provider(self, provider_name: str):
        """ Instantiate new instance of requested provider """
        try:
            self.name = provider_name
            self.module = self.registered_providers[provider_name]
        except KeyError:
            raise ValueError(f"Provider {provider_name} not registered")

        my_module = importlib.import_module(self.module)
        provider = getattr(my_module, self.name)
        return provider()

    @abstractmethod
    def create_shared_infra(self, cfg: DictConfig):
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
