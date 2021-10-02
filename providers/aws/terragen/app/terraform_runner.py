import attr
import logging
import os
import subprocess

from omegaconf import DictConfig
from providers.aws.terragen.models.terragen_models import TerragenProperties

log = logging.getLogger(__name__)


@attr.s
class TerraformRunner:

    terragen_properties: TerragenProperties = attr.ib()
    module_dir: str = attr.ib()
    working_dir: str = attr.ib()

    @classmethod
    def from_config(cls, provider_properties: DictConfig, module_dir: str):

        return cls(terragen_properties=TerragenProperties.from_properties_bag(provider_properties),
                   module_dir=module_dir,
                   working_dir=os.getcwd())

    def create_infrastructure(self):
        if not self.terragen_properties.run_terraform:
            log.info("Skipping Create Infrastructure run_terraform set to False")
            return

        os.chdir(self.module_dir)

        # Initialise Terraform
        logging.info(f"Initialising Terraform for module {self.module_dir}")
        logging.debug(f"Terraform init cmd: {self.terragen_properties.terraform_init_cmd}")
        subprocess.run(self.terragen_properties.terraform_init_cmd.split(" "), check=True)

        # TODO add a plan step here
        # Create infra
        logging.info(f"Terraform creating infrastructure for module {self.module_dir}")
        create_cmd = "terraform apply -auto-approve"
        subprocess.run(create_cmd.split(" "), check=True)

        os.chdir(self.working_dir)  # Revert to original working dir, to ensure script hydra ouputs to correct loc

    def destroy_infrastructure(self):
        pass
