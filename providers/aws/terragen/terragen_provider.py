from omegaconf import DictConfig
import logging

from providers.aws.terragen.app.terraform_factory import TerraformFactory

from providers.cloud_provider import CloudProvider
from providers.aws.terragen.app.build_templates import build_templates

log = logging.getLogger(__name__)


class TerraGen(CloudProvider):

    def create_shared_infra(self, infra_name: str, shared_infra: DictConfig):
        tf_factory = TerraformFactory.from_shared_config(module_name=infra_name,
                                                         provider_name=self.name,
                                                         shared_module=shared_infra)
        tf_factory.generate_terraform_module()
        iain = 1

        # for infra_key in shared_infra:
        #     log.info(f"Generating shared {infra_key}")
        #     shared_modules = shared_infra[infra_key]
        #
        #     for module_name in shared_modules:
        #         tf_factory = TerraformFactory.from_shared_config(module_name=module_name,
        #                                                          provider_name=self.name,
        #                                                          shared_module=shared_modules[module_name])
        #         tf_factory.generate_terraform_module()

            # TODO create factory for every shared module

            # for module_name in shared_modules:
            #     log.info(f"Generating module: {module_name}")
                #build_templates(module, self.name, shared_modules[module])
        #         tf_factory = TerraformFactory(module_name=module_name,
        #                                       provider_name=self.name,
        #                                       module_definition=shared_modules[module_name])
        #         iain = tf_factory

    def destroy_shared_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def create_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def destroy_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()
