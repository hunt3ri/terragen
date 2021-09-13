from omegaconf import DictConfig
import logging

from providers.cloud_provider import CloudProvider
from providers.aws.terragen.app.build_templates import build_templates

log = logging.getLogger(__name__)


class TerraGen(CloudProvider):

    def create_shared_infra(self, shared_infra: DictConfig):

        for infra_key in shared_infra:
            log.info(f"Parsing shared infrastructure config for: {infra_key}")
            shared_modules = shared_infra[infra_key]

            for module in shared_modules:
                log.info(f"Generating module: {module}")
                build_templates(module, self.name, shared_modules[module])

    def destroy_shared_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def create_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def destroy_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()
