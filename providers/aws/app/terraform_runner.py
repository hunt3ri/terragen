import attr
import logging
import os
import subprocess

from providers.aws.models.terragen_models import TerragenProperties

log = logging.getLogger(__name__)


@attr.s
class TerraformRunner:

    properties: TerragenProperties = attr.ib()
    hydra_dir: str = attr.ib()
    working_dir: str = attr.ib()
    tfvars_file: str = attr.ib()

    @classmethod
    def from_config(cls, properties: TerragenProperties, hydra_dir: str, tfvars_file: str):

        return cls(properties=properties, hydra_dir=hydra_dir, working_dir=os.getcwd(), tfvars_file=tfvars_file)

    def create_infrastructure(self):
        if self.properties.debug_mode:
            logging.info("Debug mode is On.  Skipping create infrastructure")
            return

        os.chdir(self.hydra_dir)

        # Initialise Terraform
        logging.info(f"Initialising Terraform for module {self.hydra_dir}")
        subprocess.run("terraform init".split(" "), check=True)

        if self.properties.terraform_plan:
            logging.info(f"Generate Terraform Plan for creating infrastructure for module {self.hydra_dir}")
            plan_cmd = f"terraform plan -var-file={self.tfvars_file} -out ./tfplan"
            logging.debug(f"Plan cmd: {plan_cmd}")
            subprocess.run(plan_cmd.split(" "), check=True)
            logging.info(f"Generating human readable tfplan.txt for {self.hydra_dir}")
            subprocess.run("terraform show tfplan -no-color > ./tfplan.txt", check=True, shell=True)
        else:
            # Create infra
            logging.info(f"Terraform creating infrastructure for module {self.hydra_dir}")
            create_cmd = f"terraform apply -var-file={self.tfvars_file} -auto-approve"
            logging.debug(f"create_cmd: {create_cmd}")
            subprocess.run(create_cmd.split(" "), check=True)

        os.chdir(self.working_dir)  # Revert to original working dir, to ensure script hydra outputs to correct loc

    def destroy_infrastructure(self):
        if self.properties.debug_mode:
            logging.info("Debug mode is On. Skipping destroy infrastructure")
            return

        os.chdir(self.hydra_dir)

        # Initialise Terraform
        logging.info(f"Initialising Terraform for module {self.hydra_dir}")
        subprocess.run("terraform init".split(" "), check=True)

        if self.properties.terraform_plan:
            logging.info(f"Generate Terraform Plan for destroying infrastructure for module {self.hydra_dir}")
            subprocess.run(f"terraform plan -destroy -var-file={self.tfvars_file} -out ./tfplan".split(" "), check=True)
            logging.info(f"Generating human readable tfplan.txt for {self.hydra_dir}")
            subprocess.run("terraform show tfplan -no-color > ./tfplan.txt", check=True, shell=True)
        else:
            logging.info(f"Terraform destroying infrastructure for module {self.hydra_dir}")
            destroy_cmd = f"terraform destroy -var-file={self.tfvars_file} -auto-approve"
            subprocess.run(destroy_cmd.split(" "), check=True)

        os.chdir(self.working_dir)  # Revert to original working dir, to ensure script hydra outputs to correct loc
