import attr
import logging
import os

from distutils.dir_util import copy_tree
from jinja2 import Environment, PackageLoader, select_autoescape
from omegaconf import DictConfig

from providers.was.app.utils import to_toml
from providers.was.models.terragen_models import TerragenProperties
from providers.aws.app.lookup_handler import LookupHandler

log = logging.getLogger(__name__)


@attr.s
class TerraformFactory:

    properties: TerragenProperties = attr.ib()
    module_name: str = attr.ib()
    hydra_dir: str = attr.ib()  # The Hydra output dir
    module_config: DictConfig = attr.ib()
    module_metadata: DictConfig = attr.ib()
    service_name: str = attr.ib()

    # Init Jinja to load templates
    _env = Environment(
        loader=PackageLoader("providers.aws"),
        autoescape=select_autoescape(),
    )

    # Register Jinja helper functions
    _env.globals["to_toml"] = to_toml

    @classmethod
    def from_config(cls, module_config: DictConfig, properties: TerragenProperties):
        """Construct TerraformFactory from Hydra Shared Config"""
        module_metadata = module_config.module_metadata
        module_name = module_metadata.name
        service_name = module_metadata.aws_service

        log.info(f"Instantiating TerraformFactory for: {service_name}/{module_metadata.name}")
        hydra_dir = f"{os.getcwd()}/{properties.provider_name}/{properties.environment}/{service_name}/{module_name}"

        return cls(
            module_name=module_name,
            module_config=module_config.config,
            service_name=service_name,
            properties=properties,
            hydra_dir=hydra_dir,
            module_metadata=module_metadata,
        )

    def generate_terraform_templates(self):
        log.info(f"Generating Terraform templates for: {self.module_name}")
        log.info(f"Template files will be written to: {self.hydra_dir}")

        os.makedirs(self.hydra_dir, exist_ok=True)
        self.generate_terraform_config_file()
        self.copy_module_to_outputs()
        # self.generate_terraform_module()
        # self.generate_terraform_resource()

    def generate_terraform_config_file(self):
        tf_config_template = self._env.get_template("terraform_config.jinja")
        tf_config_path = f"{self.hydra_dir}/terraform_config.tf"
        log.info("Generating terraform_config.tf")

        # TODO this assumes S3 backend
        self.properties.backend.key = f"{self.module_metadata.statefile}/terraform.tfstate"

        with open(tf_config_path, "w") as tf_config_file:
            tf_config_file.write(
                tf_config_template.render(backend=str(self.properties.backend), provider=str(self.properties.provider))
            )

    def copy_module_to_outputs(self):
        cwd = os.getcwd()
        iain = os.listdir(f"../../../{self.module_metadata.module_dir}")
        bob = iain
        copy_tree(f"../../../{self.module_metadata.module_dir}", self.hydra_dir)
