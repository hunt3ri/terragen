from omegaconf import DictConfig
import logging

from providers.aws.terragen.app.terraform_factory import TerraformFactory
from providers.aws.terragen.app.terraform_runner import TerraformRunner
from providers.aws.terragen.models.terragen_models import TerragenProperties
from providers.cloud_provider import CloudProvider


log = logging.getLogger(__name__)


class TerraGen(CloudProvider):

    def create_shared_infra(self, service_name: str, infra_name: str, shared_infra: DictConfig):
        properties = TerragenProperties.from_properties(debug_mode=self.debug_mode,
                                                        environment=self.environment,
                                                        provider_name=self.provider_name,
                                                        provider_properties=self.provider_properties)

        tf_factory = TerraformFactory.from_shared_config(module_name=infra_name,
                                                         shared_module=shared_infra,
                                                         service_name=service_name,
                                                         properties=properties)
        tf_factory.generate_terraform_templates()

        # # TODO properties need to go to factory
        # tf_runner = TerraformRunner.from_config(provider_properties=self.provider_properties,
        #                                         module_dir=tf_factory.module_dir)
        # tf_runner.create_infrastructure()


    def destroy_shared_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def create_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def destroy_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()
