import attr
import logging
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from omegaconf import DictConfig, ListConfig

from providers.terragen.app.utils import to_toml, get_lookup_values
from providers.terragen.models.terragen_models import TerragenProperties

log = logging.getLogger(__name__)


@attr.s
class TerraformFactory:

    properties: TerragenProperties = attr.ib()
    module_name: str = attr.ib()
    hydra_dir: str = attr.ib()      # The Hydra output dir
    module_config: DictConfig = attr.ib()
    module_metadata: DictConfig = attr.ib()
    outputs: DictConfig = attr.ib()
    service_name: str = attr.ib()

    # Init Jinja to load templates
    _env = Environment(
        loader=PackageLoader("providers.terragen"),
        autoescape=select_autoescape(),
    )

    # Register Jinja helper functions
    _env.globals["to_toml"] = to_toml

    @classmethod
    def from_shared_config(cls, shared_module: DictConfig, properties: TerragenProperties):
        """ Construct TerraformFactory from Hydra Shared Config"""
        module_metadata = shared_module.module_metadata
        module_name = module_metadata.name
        service_name = module_metadata.aws_service

        log.info(f"Instantiating TerraformFactory for: {service_name}/{module_metadata.name}")
        hydra_dir = f"{os.getcwd()}/{properties.provider_name}/{properties.environment}/{service_name}/{module_name}"

        return cls(module_name=module_name, module_config=shared_module.config, service_name=service_name,
                   properties=properties, hydra_dir=hydra_dir, outputs=shared_module.outputs,
                   module_metadata=module_metadata)

    def generate_terraform_templates(self):
        log.info(f"Generating Terraform templates for: {self.module_name}")
        log.info(f"Template files will be written to: {self.hydra_dir}")

        os.makedirs(self.hydra_dir, exist_ok=True)
        self.generate_terraform_config_file()
        self.generate_terraform_module()
        self.generate_terraform_resource()

    def generate_terraform_config_file(self):
        tf_config_template = self._env.get_template("terraform_config.jinja")
        tf_config_path = f"{self.hydra_dir}/terraform_config.tf"
        log.info(f"Generating terraform_config.tf")

        # TODO this assumes S3 backend
        backend_key = str(self.module_metadata.lookup).replace(".", "/")
        self.properties.backend.key = f"{backend_key}/terraform.tfstate"

        with open(tf_config_path, 'w') as tf_config_file:
            tf_config_file.write(tf_config_template.render(backend=str(self.properties.backend),
                                                           provider=str(self.properties.provider)))

    def lookup_handler(self):
        log.info(f"Handling lookups for service: {self.service_name} module: {self.module_name}")
        lookups = {}
        for key, value in self.module_config.items():
            if isinstance(value, bool):
                continue  # Bools are not iterable so skip
            elif isinstance(value, ListConfig):
                # iain = value[0]
                # abi = iain
                continue
            elif "lookup" in value:
                lookups[key] = value
                # TODO parse values in Lists

        if len(lookups) == 0:
            log.info(f"No lookups found in {self.module_name}.tf")
            return

        for key, lookup in lookups.items():
            log.info(f"Processing lookup: {lookup}")
            datablock_key, datablock_lookup = get_lookup_values(lookup)
            self.generate_terraform_data_block(datablock_key)
            self.module_config[key] = f"data.terraform_remote_state.{self.module_name}.{datablock_lookup}"

    def generate_terraform_data_block(self, datablock_key: str):
        self.properties.backend.key = f"{datablock_key}/terraform.tfstate"

        tf_module_file_path = f"{self.hydra_dir}/data.tf"
        tf_datablock_template = self._env.get_template("data.jinja")

        with open(tf_module_file_path, 'w') as tf_module_file:
            tf_module_file.write(tf_datablock_template.render(module_name=self.module_name,
                                                              backend=self.properties.backend.as_datablock()))

    def generate_terraform_module(self):
        if "module_source" not in self.module_metadata:
            return

        self.lookup_handler()
        self.generate_terraform_outputs("module")

        tags = self.module_config.tags
        tf_module_file_path = f"{self.hydra_dir}/{self.module_name}.tf"
        tf_module_template = self._env.get_template("module.jinja")
        log.info(f"Generating module {self.module_name}.tf")

        with open(tf_module_file_path, 'w') as tf_module_file:
            tf_module_file.write(tf_module_template.render(module_name=self.module_name,
                                                           module_config=self.module_config,
                                                           module_url=self.module_metadata.module_url,
                                                           module_source=self.module_metadata.module_source,
                                                           module_version=self.module_metadata.module_version,
                                                           tags=tags))

    def generate_terraform_outputs(self, module_type: str):
        if self.outputs is None:
            log.info(f"Module {self.module_name} has no Outputs defined")
            return  # No outputs to generate

        # TODO rework outputs to be more lookup friendly
        tf_outputs_template = self._env.get_template("outputs.jinja")
        tf_outputs_file_path = f"{self.hydra_dir}/outputs.tf"
        log.info(f"Generating outputs.tf")

        with open(tf_outputs_file_path, 'w') as tf_outputs_file:
            tf_outputs_file.write(tf_outputs_template.render(module_type=module_type,
                                                             module_name=self.module_name,
                                                             outputs=self.outputs))

    def generate_terraform_resource(self):
        if "resource_type" not in self.module_metadata:
            return

        self.lookup_handler()
        self.generate_terraform_outputs(self.module_metadata.resource_type)

        tf_resource_file_path = f"{self.hydra_dir}/{self.module_name}.tf"
        tf_resource_template = self._env.get_template("resource.jinja")
        log.info(f"Generating resource {self.module_name}.tf")

        with open(tf_resource_file_path, 'w') as tf_resource_file:
            tf_resource_file.write(tf_resource_template.render(resource_type=self.module_metadata.resource_type,
                                                               module_config=self.module_config,
                                                               module_name=self.module_name))


