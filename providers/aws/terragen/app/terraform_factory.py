import attr
import logging
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@attr.s
class TerraformFactory:

    module_name: str = attr.ib()
    module_path: str = attr.ib()
    module_config: DictConfig = attr.ib()
    provider_name: str = attr.ib()
    provider_config: DictConfig = attr.ib()

    _env = Environment(
        loader=PackageLoader("providers.aws.terragen"),
        autoescape=select_autoescape()
    )

    @classmethod
    def from_shared_config(cls, module_name: str, provider_name: str, shared_module: DictConfig):
        """ Construct TerraformFactory from Hydra Shared Config"""
        log.info(f"Instantiating TerraformFactory for: {module_name}")
        module_config = shared_module.config
        provider_config = shared_module.providers[provider_name]
        module_path = f"{provider_config.module_path}/{module_name}"
        return cls(module_name=module_name, module_path=module_path, module_config=module_config,
                   provider_name=provider_name, provider_config=provider_config)

    def generate_terraform_module(self):
        log.info(f"Generating Terraform Module for: {self.module_name}")
        log.info(f"Module files will be written to: {self.module_path}")
        os.makedirs(self.module_path, exist_ok=True)

        self.generate_terraform_config_file()

    def generate_terraform_config_file(self):
        tf_config_template = self._env.get_template("terraform_config.tf")
        tf_config_path = f"{self.module_path}/terraform_config.tf"
        log.info(f"Generating terraform_config.tf")

        iain = os.getcwd()

        s3_backend_key = f"{self.provider_config.s3_backend_root}/{self.module_name}"
        with open(tf_config_path, 'w') as tf_config_file:
            tf_config_file.write(tf_config_template.render(s3_backend_key=s3_backend_key))



