import attr
import logging
import os
import subprocess

from terragen.providers.aws.models.aws_models import AWSModule
from terragen.providers.cloud_provider import BuildConfig

log = logging.getLogger(__name__)


@attr.s
class TerraformLauncher:

    build_config: BuildConfig = attr.ib()
    aws_module: AWSModule = attr.ib()
    working_dir: str = attr.ib()
    # hydra_dir: str = attr.ib()
    # working_dir: str = attr.ib()
    # tfvars_file: str = attr.ib()

    @classmethod
    def from_config(cls, build_config: BuildConfig, aws_module: AWSModule):
        return cls(build_config=build_config, aws_module=aws_module, working_dir=os.getcwd())

    def create_infrastructure(self):
        if self.build_config.debug_mode:
            logging.info("Debug mode is On.  Skipping create infrastructure")
            return

        os.chdir(self.aws_module.hydra_dir)

        # Initialise Terraform
        logging.info(f"Initialising Terraform for module {self.aws_module.hydra_dir}")
        subprocess.run("terraform init".split(" "), check=True)

        if self.build_config.terraform_mode == "plan":
            logging.info(f"Generate Terraform Plan for creating infrastructure for module {self.aws_module.hydra_dir}")
            plan_cmd = f"terraform plan -var-file={self.aws_module.tfvars_file} -out ./tfplan"
            logging.debug(f"Plan cmd: {plan_cmd}")
            subprocess.run(plan_cmd.split(" "), check=True)
            logging.info(f"Generating human readable tfplan.txt for {self.aws_module.hydra_dir}")
            subprocess.run("terraform show tfplan -no-color > ./tfplan.txt", check=True, shell=True)
        else:
            # Create infra
            logging.info(f"Terraform creating infrastructure for module {self.aws_module.hydra_dir}")
            create_cmd = f"terraform apply -var-file={self.aws_module.tfvars_file} -auto-approve"
            logging.debug(f"create_cmd: {create_cmd}")
            subprocess.run(create_cmd.split(" "), check=True)

        os.chdir(self.working_dir)  # Revert to original working dir, to ensure script hydra outputs to correct loc

    def destroy_infrastructure(self):
        if self.build_config.debug_mode:
            logging.info("Debug mode is On. Skipping destroy infrastructure")
            return

        os.chdir(self.aws_module.hydra_dir)

        # Initialise Terraform
        logging.info(f"Initialising Terraform for module {self.aws_module.hydra_dir}")
        subprocess.run("terraform init".split(" "), check=True)

        if self.build_config.terraform_mode == "plan":
            logging.info(f"Generate Terraform Plan for destroying infrastructure for module {self.aws_module.hydra_dir}")
            subprocess.run(f"terraform plan -destroy -var-file={self.aws_module.tfvars_file} -out ./tfplan".split(" "), check=True)
            logging.info(f"Generating human readable tfplan.txt for {self.aws_module.hydra_dir}")
            subprocess.run("terraform show tfplan -no-color > ./tfplan.txt", check=True, shell=True)
        else:
            logging.info(f"Terraform destroying infrastructure for module {self.aws_module.hydra_dir}")
            destroy_cmd = f"terraform destroy -var-file={self.aws_module.tfvars_file} -auto-approve"
            subprocess.run(destroy_cmd.split(" "), check=True)

        os.chdir(self.working_dir)  # Revert to original working dir, to ensure script hydra outputs to correct loc
