from omegaconf import DictConfig
import logging

from terragen.providers.aws.app.terraform_factory import TerraformFactory
from terragen.providers.aws.app.terraform_launcher import TerraformLauncher
from terragen.providers.aws.models.terragen_models import AWSEnvironment
from terragen.providers.cloud_provider import CloudProvider


log = logging.getLogger(__name__)


class AWSProvider(CloudProvider):

    aws_environment: AWSEnvironment
    terraform_launcher: TerraformLauncher

    def create_infra(self, module_config: DictConfig):
        self.aws_environment = AWSEnvironment.from_environment_config(self.environment_config, module_config.module_metadata)
        self.terraform_launcher = self.set_terraform_launcher(module_config)
        self.terraform_launcher.create_infrastructure()

    def destroy_infra(self, module_config: DictConfig):
        self.aws_environment = AWSEnvironment.from_environment_config(self.environment_config,
                                                                      module_config.module_metadata)
        self.terraform_launcher = self.set_terraform_launcher(module_config)
        self.terraform_launcher.destroy_infrastructure()

    def set_terraform_launcher(self, cloud_config: DictConfig) -> TerraformLauncher:

        tf_factory = TerraformFactory.from_config(module_config=cloud_config,
                                                  build_config=self.build_config,
                                                  aws_environment=self.aws_environment)
        tf_factory.generate_terraform_templates()
        tf_launcher = TerraformLauncher.from_config(
            build_config=self.build_config, hydra_dir=tf_factory.hydra_dir, tfvars_file=tf_factory.tfvars_file
        )

        return tf_launcher
