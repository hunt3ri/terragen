import attr
import logging
import os
import subprocess

from providers.aws.terragen.models.terragen_models import TerragenProperties

log = logging.getLogger(__name__)


@attr.s
class TerraformRunner:

    properties: TerragenProperties = attr.ib()
    module_dir: str = attr.ib()
    working_dir: str = attr.ib()

    @classmethod
    def from_config(cls, properties: TerragenProperties, module_dir: str):

        return cls(properties=properties,
                   module_dir=module_dir,
                   working_dir=os.getcwd())

    def create_infrastructure(self):
        if not self.properties.run_terraform:
            log.info("Skipping Create Infrastructure run_terraform set to False")
            return

        os.chdir(self.module_dir)

        # Initialise Terraform
        logging.info(f"Initialising Terraform for module {self.module_dir}")
        subprocess.run("terraform init".split(" "), check=True)

        # TODO add a plan step here
        # Create infra
        logging.info(f"Terraform creating infrastructure for module {self.module_dir}")
        create_cmd = "terraform apply -auto-approve"
        subprocess.run(create_cmd.split(" "), check=True)

        os.chdir(self.working_dir)  # Revert to original working dir, to ensure script hydra ouputs to correct loc

    def destroy_infrastructure(self):
        pass