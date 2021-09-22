import attr
import logging
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from omegaconf import DictConfig


log = logging.getLogger(__name__)


@attr.s
class TerraformFactory:

    environment: str = attr.ib()
    module_name: str = attr.ib()
    module_path: str = attr.ib()
    module_config: DictConfig = attr.ib()
    provider_name: str = attr.ib()
    provider_config: DictConfig = attr.ib()
    debug_mode: bool = attr.ib(default=False)

    # Init Jinja to load templates
    _env = Environment(
        loader=PackageLoader("providers.aws.terragen"),
        autoescape=select_autoescape()
    )

    @classmethod
    def from_shared_config(cls, module_name: str, provider_name: str, shared_module: DictConfig, debug_mode: bool,
                           environment: str):
        """ Construct TerraformFactory from Hydra Shared Config"""
        log.info(f"Instantiating TerraformFactory for: {module_name}")
        module_config = shared_module.config
        provider_config = shared_module.providers[provider_name]

        # If debug on, write TF files to hydra output dir
        if debug_mode:
            module_root = os.getcwd()
        else:
            module_root = provider_config.module_path

        module_path = f"{module_root}/{provider_name}/{environment}/{module_name}"

        return cls(module_name=module_name, module_path=module_path, module_config=module_config,
                   provider_name=provider_name, provider_config=provider_config, debug_mode=debug_mode,
                   environment=environment)

    def generate_terraform_templates(self):
        log.info(f"Generating Terraform templates for: {self.module_name}")
        log.info(f"Template files will be written to: {self.module_path}")
        os.makedirs(self.module_path, exist_ok=True)

        self.generate_terraform_config_file()
        self.generate_terraform_module()

    def generate_terraform_config_file(self):
        tf_config_template = self._env.get_template("terraform_config.tf")
        tf_config_path = f"{self.module_path}/terraform_config.tf"
        log.info(f"Generating terraform_config.tf")

        s3_backend_key = f"{self.provider_config.s3_backend_root}/{self.module_name}"
        with open(tf_config_path, 'w') as tf_config_file:
            tf_config_file.write(tf_config_template.render(s3_backend_key=s3_backend_key))

    def generate_terraform_module(self):
        tags = self.module_config.tags
        del self.module_config.tags  # Remove tags from dictionary so template doesn't render them incorrectly

        tf_module_file_path = f"{self.module_path}/{self.module_name}.tf"
        tf_module_template = self._env.get_template("module.tf")
        log.info(f"Generating: {self.module_name}.tf")

        with open(tf_module_file_path, 'w') as tf_module_file:
            tf_module_file.write(tf_module_template.render(module_name=self.module_name,
                                                           module_config=self.module_config,
                                                           module_url=self.provider_config.module_url,
                                                           module_source=self.provider_config.module_source,
                                                           module_version=self.provider_config.module_version,
                                                           tags=tags))
