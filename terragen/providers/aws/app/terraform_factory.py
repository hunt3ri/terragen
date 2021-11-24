import attr
import logging
import os

from distutils.dir_util import copy_tree
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from omegaconf import DictConfig
from pathlib import Path

from terragen.providers.aws.app.utils import to_toml
from terragen.providers.aws.models.terragen_models import TerragenProperties

log = logging.getLogger(__name__)


@attr.s
class TerraformFactory:

    properties: TerragenProperties = attr.ib()
    module_name: str = attr.ib()
    hydra_dir: str = attr.ib()  # The Hydra output dir
    module_config: DictConfig = attr.ib()
    module_metadata: DictConfig = attr.ib()
    service_name: str = attr.ib()
    tfvars_file: str = attr.ib()
    lookups: DictConfig = attr.ib()

    # Init Jinja to load templates from local package
    jinja_package_env = Environment(loader=PackageLoader("terragen.providers.aws"), autoescape=select_autoescape())

    # Register Jinja helper functions
    jinja_package_env.globals["to_toml"] = to_toml

    @classmethod
    def from_config(cls, module_config: DictConfig, properties: TerragenProperties):
        """Construct TerraformFactory from Hydra Shared Config"""
        module_metadata = module_config.module_metadata
        module_name = module_metadata.name
        service_name = module_metadata.aws_service
        properties.backend.state_file = module_metadata.state_file

        log.info(f"Instantiating TerraformFactory for: {service_name}/{module_metadata.name}")

        # Create path for outputting tf modules within hydra output dir
        hydra_dir = Path(
            f"{os.getcwd()}/{properties.provider_name}/{properties.environment}/{service_name}/{module_name}"
        )

        return cls(
            module_name=module_name,
            module_config=module_config.config,
            service_name=service_name,
            properties=properties,
            hydra_dir=str(hydra_dir),
            module_metadata=module_metadata,
            tfvars_file=f"{module_name}.tfvars",
            lookups=module_config.lookups,
        )

    def generate_terraform_templates(self):
        log.info(f"Generating Terraform templates for: {self.module_name}")
        log.info(f"Template files will be written to: {self.hydra_dir}")

        os.makedirs(self.hydra_dir, exist_ok=True)

        # Copy all module files to hydra outputs
        copy_tree(f"../../../{self.module_metadata.module_dir}", self.hydra_dir)
        self.generate_terraform_config_file()
        self.generate_tfvars_file()
        self.generate_data_block()

    def generate_terraform_config_file(self):
        tf_config_template = self.jinja_package_env.get_template("config.jinja")
        tf_config_path = f"{self.hydra_dir}/terraform_config.tf"
        log.info("Generating terraform_config.tf")

        # TODO assumes S3 backend
        with open(tf_config_path, "w") as tf_config_file:
            tf_config_file.write(
                tf_config_template.render(
                    profile=self.properties.backend.profile,
                    region=self.properties.backend.region,
                    bucket=self.properties.backend.bucket,
                    state_file=self.properties.backend.state_file,
                )
            )

    def generate_tfvars_file(self):
        tfvars_file_path = f"{self.hydra_dir}/{self.tfvars_file}"
        tfvars_template = self.jinja_package_env.get_template("tfvars.jinja")
        log.info(f"Generating module {self.tfvars_file}")

        with open(tfvars_file_path, "w") as tfvars_file:
            tfvars_file.write(tfvars_template.render(module_config=self.module_config))

    def generate_data_block(self):
        if self.lookups is None:
            log.info(f"No lookups to process for module {self.module_name}")
            return

        log.info(f"Generating datablock for {self.module_name}")

        # For data blocks we need to load template from module directory in Hydra output dir rather than local package
        jinja_fs_env = Environment(
            loader=FileSystemLoader([self.hydra_dir]),
            autoescape=select_autoescape(),
        )

        data_block_file = f"{self.hydra_dir}/data.tf"
        data_template = jinja_fs_env.get_template("data.tf")

        with open(data_block_file, "w") as data_file:
            data_file.write(
                data_template.render(
                    lookups=self.lookups,
                    profile=self.properties.backend.profile,
                    region=self.properties.backend.region,
                    bucket=self.properties.backend.bucket,
                )
            )
