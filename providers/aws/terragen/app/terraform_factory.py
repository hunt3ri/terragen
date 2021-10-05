import attr
import logging
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from omegaconf import DictConfig

from providers.aws.terragen.app.utils import to_toml
from providers.aws.terragen.models.terragen_models import TerragenProperties

log = logging.getLogger(__name__)


@attr.s
class TerraformFactory:

    properties: TerragenProperties = attr.ib()
    module_name: str = attr.ib()
    module_dir: str = attr.ib()     # The directory terraform files will be written and executed from
    hydra_dir: str = attr.ib()      # The Hydra output dir, so we can have a history of changes
    output_dirs: list[str] = attr.ib()
    module_config: DictConfig = attr.ib()
    provider_config: DictConfig = attr.ib()
    service_name: str = attr.ib()

    # Init Jinja to load templates
    _env = Environment(
        loader=PackageLoader("providers.aws.terragen"),
        autoescape=select_autoescape()
    )

    # Register helper functions
    _env.globals["to_toml"] = to_toml

    @classmethod
    def from_shared_config(cls, service_name: str, module_name: str, shared_module: DictConfig,
                           properties: TerragenProperties):
        """ Construct TerraformFactory from Hydra Shared Config"""

        log.info(f"Instantiating TerraformFactory for: {service_name}/{module_name}")
        module_config = shared_module.config
        provider_config = shared_module.providers[properties.provider_name]

        # If debug on, write TF files to hydra output dir
        # if properties.debug_mode:
        #     module_root = os.getcwd()
        # else:
        #     module_root = provider_config.module_path

        hydra_dir = f"{os.getcwd()}/{properties.provider_name}/{properties.environment}/{service_name}/{module_name}"
        module_dir = f"{provider_config.module_path}/{properties.provider_name}/{properties.environment}/{service_name}/{module_name}"

        # If running terraform generate templates and a hydra copy, otherwise just the hydra copy
        if properties.run_terraform:
            output_dirs = [hydra_dir, module_dir]
        else:
            output_dirs = [hydra_dir]

        return cls(module_name=module_name, module_dir=module_dir, module_config=module_config,
                   provider_config=provider_config, service_name=service_name, properties=properties,
                   hydra_dir=hydra_dir, output_dirs=output_dirs)

    def generate_terraform_templates(self):
        log.info(f"Generating Terraform templates for: {self.module_name}")
        log.info(f"Template files will be written to: {self.module_dir}")

        for directory in self.output_dirs:
            os.makedirs(directory, exist_ok=True)
            self.generate_terraform_config_file(directory)
            self.generate_terraform_outputs(directory)
            self.generate_terraform_module(directory)
            self.generate_terraform_resource(directory)

    def generate_terraform_config_file(self, directory: str):
        tf_config_template = self._env.get_template("terraform_config.tf")
        tf_config_path = f"{directory}/terraform_config.tf"
        log.info(f"Generating terraform_config.tf")

        # TODO this assumes S3 backend
        self.properties.backend.key = f"{self.provider_config.s3_backend_root}/{self.module_name}/terraform.tfstate"

        with open(tf_config_path, 'w') as tf_config_file:
            tf_config_file.write(tf_config_template.render(backend=str(self.properties.backend),
                                                           provider=str(self.properties.provider)))

    def generate_terraform_module(self, directory: str):
        if "module_source" not in self.provider_config:
            return

        tags = self.module_config.tags
        del self.module_config.tags  # Remove tags from dictionary so template doesn't render them incorrectly

        tf_module_file_path = f"{directory}/{self.module_name}.tf"
        tf_module_template = self._env.get_template("module.tf")
        log.info(f"Generating module {self.module_name}.tf")

        with open(tf_module_file_path, 'w') as tf_module_file:
            tf_module_file.write(tf_module_template.render(module_name=self.module_name,
                                                           module_config=self.module_config,
                                                           module_url=self.provider_config.module_url,
                                                           module_source=self.provider_config.module_source,
                                                           module_version=self.provider_config.module_version,
                                                           tags=tags))

    def generate_terraform_outputs(self, directory: str):
        if "outputs" not in self.provider_config:
            return  # No outputs to generate

        outputs = self.provider_config.outputs
        tf_outputs_template = self._env.get_template("outputs.tf")
        tf_outputs_file_path = f"{directory}/outputs.tf"
        log.info(f"Generating outputs.tf")

        with open(tf_outputs_file_path, 'w') as tf_outputs_file:
            tf_outputs_file.write(tf_outputs_template.render(module_name=self.module_name,
                                                             outputs=outputs))

    def generate_terraform_resource(self, directory: str):
        if "resource_type" not in self.provider_config:
            return

        tf_resource_file_path = f"{directory}/{self.module_name}.tf"
        tf_resource_template = self._env.get_template("resource.tf")
        log.info(f"Generating resource {self.module_name}.tf")

        with open(tf_resource_file_path, 'w') as tf_resource_file:
            tf_resource_file.write(tf_resource_template.render(resource_type=self.provider_config.resource_type,
                                                               module_config=self.module_config,
                                                               module_name=self.module_name))
