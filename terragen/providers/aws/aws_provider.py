from omegaconf import DictConfig
import logging

from terragen.providers.aws.app.terraform_factory import TerraformFactory
from terragen.providers.aws.app.terraform_runner import TerraformRunner
from terragen.providers.aws.models.terragen_models import TerragenProperties
from terragen.providers.cloud_provider import CloudProvider


log = logging.getLogger(__name__)


class AWSProvider(CloudProvider):
    def create_infra(self, cloud_config: DictConfig, environment_config: DictConfig):
        tf_runner = self.get_terraform_runner(cloud_config, environment_config)
        tf_runner.create_infrastructure()

    def destroy_infra(self, cloud_config: DictConfig, environment_config: DictConfig):
        tf_runner = self.get_terraform_runner(cloud_config, environment_config)
        tf_runner.destroy_infrastructure()

    def get_terraform_runner(self, cloud_config: DictConfig, environment_config: DictConfig) -> TerraformRunner:
        properties = TerragenProperties.from_properties(
            debug_mode=self.debug_mode,
            environment=self.environment,
            provider_name=self.provider_name,
            provider_properties=self.provider_properties,
        )

        tf_factory = TerraformFactory.from_config(module_config=cloud_config, properties=properties)
        tf_factory.generate_terraform_templates()

        tf_runner = TerraformRunner.from_config(
            properties=properties, hydra_dir=tf_factory.hydra_dir, tfvars_file=tf_factory.tfvars_file
        )

        return tf_runner
