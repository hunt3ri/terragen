from omegaconf import DictConfig

from providers.cloud_provider import CloudProvider


class AWSTerraformProvider(CloudProvider):

    def create_shared_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def destroy_shared_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def create_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def destroy_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()
