import attr
import logging
import os

from distutils.dir_util import copy_tree
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from omegaconf import DictConfig

from terragen.providers.aws.app.utils import to_toml
from terragen.providers.aws.models.aws_models import AWSEnvironment, AWSModule
from terragen.providers.cloud_provider import BuildConfig


log = logging.getLogger(__name__)


@attr.s
class TerraformFactory:

    build_config: BuildConfig = attr.ib()
    aws_environment: AWSEnvironment = attr.ib()
    aws_module: AWSModule = attr.ib()

    # TODO these properties could be a class
    # module_name: str = attr.ib()
    # hydra_dir: str = attr.ib()  # The Hydra output dir
    # module_config: DictConfig = attr.ib()
    # module_metadata: DictConfig = attr.ib()
    # service_name: str = attr.ib()
    # tfvars_file: str = attr.ib()
    # lookups: DictConfig = attr.ib()

    # Init Jinja to load templates from local package
    jinja_package_env = Environment(loader=PackageLoader("terragen.providers.aws"), autoescape=select_autoescape())

    # Register Jinja helper functions
    jinja_package_env.globals["to_toml"] = to_toml

    @classmethod
    def from_config(cls, module_config: DictConfig, build_config: BuildConfig, aws_environment: AWSEnvironment):
        """Construct TerraformFactory from Hydra Shared Config"""
        aws_module = AWSModule.from_config(module_config, build_config)
        log.info(f"Instantiating TerraformFactory for: {aws_module.service_name}/{aws_module.module_metadata.name}")

        return cls(
            aws_module=aws_module,
            build_config=build_config,
            aws_environment=aws_environment,
        )

    def generate_terraform_templates(self):
        log.info(f"Generating Terraform templates for: {self.aws_module.module_name}")
        log.info(f"Template files will be written to: {self.aws_module.hydra_dir}")

        os.makedirs(self.aws_module.hydra_dir, exist_ok=True)

        # Copy all module files to hydra outputs
        log.debug(f"Current Working Dir: {os.getcwd()}")
        copy_tree(f"../../../{self.aws_module.module_metadata.module_dir}", self.aws_module.hydra_dir)
        self.generate_terraform_config_file()
        self.generate_tfvars_file()
        self.generate_data_block()

    def generate_terraform_config_file(self):
        tf_config_template = self.jinja_package_env.get_template("config.jinja")
        tf_config_path = f"{self.aws_module.hydra_dir}/terraform_config.tf"
        log.info("Generating terraform_config.tf")

        # TODO assumes S3 backend
        with open(tf_config_path, "w") as tf_config_file:
            tf_config_file.write(
                tf_config_template.render(
                    profile=self.aws_environment.profile,
                    region=self.aws_environment.region,
                    bucket=self.aws_environment.bucket,
                    state_file=self.aws_environment.state_file,
                )
            )

    def generate_tfvars_file(self):
        tfvars_file_path = f"{self.aws_module.hydra_dir}/{self.aws_module.tfvars_file}"
        tfvars_template = self.jinja_package_env.get_template("tfvars.jinja")
        log.info(f"Generating module {self.aws_module.tfvars_file}")

        with open(tfvars_file_path, "w") as tfvars_file:
            tfvars_file.write(tfvars_template.render(module_config=self.aws_module.module_config))

    def generate_data_block(self):
        if self.aws_module.lookups is None:
            log.info(f"No lookups to process for module {self.aws_module.module_name}")
            return

        log.info(f"Generating datablock for {self.aws_module.module_name}")

        # For data blocks we need to load template from module directory in Hydra output dir rather than local package
        jinja_fs_env = Environment(
            loader=FileSystemLoader([self.aws_module.hydra_dir]),
            autoescape=select_autoescape(),
        )

        data_block_file = f"{self.aws_module.hydra_dir}/data.tf"
        data_template = jinja_fs_env.get_template("data.tf")

        with open(data_block_file, "w") as data_file:
            data_file.write(
                data_template.render(
                    lookups=self.aws_module.lookups,
                    profile=self.aws_environment.profile,
                    region=self.aws_environment.region,
                    bucket=self.aws_environment.bucket,
                )
            )
