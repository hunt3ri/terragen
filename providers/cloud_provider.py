from abc import ABC, abstractmethod
from omegaconf import DictConfig


class CloudProvider(ABC):

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
