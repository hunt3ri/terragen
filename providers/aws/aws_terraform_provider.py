from omegaconf import DictConfig

from providers.cloud_provider import CloudProvider


class AWSTerraformProvider(CloudProvider):
    def create_shared_infra(self, cfg: DictConfig):
        pass

    def destroy_shared_infra(self, cfg: DictConfig):
        pass

    def create_app_infra(self, cfg: DictConfig):
        pass

    def destroy_app_infra(self, cfg: DictConfig):
        pass