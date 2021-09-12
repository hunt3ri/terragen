from omegaconf import DictConfig

from providers.cloud_provider import CloudProvider
from providers.aws.terragen.app.build_templates import build_templates


class TerraGen(CloudProvider):

    def create_shared_infra(self, shared_infra: DictConfig):

        for infra_key in shared_infra:
            abi = infra_key
            build_templates(shared_infra[infra_key], self.name)

    def destroy_shared_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def create_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def destroy_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()
