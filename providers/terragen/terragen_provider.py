from omegaconf import DictConfig
import logging

from providers.terragen.app.terraform_factory import TerraformFactory
from providers.terragen.app.terraform_runner import TerraformRunner
from providers.terragen.models.terragen_models import TerragenProperties
from providers.cloud_provider import CloudProvider


log = logging.getLogger(__name__)


class TerraGen(CloudProvider):

    def create_infra(self, service_name: str, infra_name: str, shared_infra: DictConfig):
        tf_runner = self.get_terraform_runner(service_name, infra_name, shared_infra)
        tf_runner.create_infrastructure()

    def destroy_infra(self, service_name: str, infra_name: str, shared_infra: DictConfig):
        tf_runner = self.get_terraform_runner(service_name, infra_name, shared_infra)
        tf_runner.destroy_infrastructure()

    def create_app_infra(self, service_name: str, infra_name: str, shared_infra: DictConfig):
        raise NotImplementedError()

    def destroy_app_infra(self, cfg: DictConfig):
        raise NotImplementedError()

    def get_terraform_runner(self, service_name: str, infra_name: str, shared_infra: DictConfig) -> TerraformRunner:
        properties = TerragenProperties.from_properties(debug_mode=self.debug_mode,
                                                        environment=self.environment,
                                                        provider_name=self.provider_name,
                                                        provider_properties=self.provider_properties)

        tf_factory = TerraformFactory.from_shared_config(module_name=infra_name,
                                                         shared_module=shared_infra,
                                                         service_name=service_name,
                                                         properties=properties)
        tf_factory.generate_terraform_templates()

        tf_runner = TerraformRunner.from_config(properties=properties,
                                                hydra_dir=tf_factory.hydra_dir)

        return tf_runner