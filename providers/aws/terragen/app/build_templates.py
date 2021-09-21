import logging
import os
from jinja2 import Environment, PackageLoader, select_autoescape
from omegaconf import DictConfig

log = logging.getLogger(__name__)

# Jinja2 environment to load templates
env = Environment(
    loader=PackageLoader("providers.aws.terragen"),
    autoescape=select_autoescape()
)

tf_module_template = env.get_template("module.tf")


def generate_terraform_outputs(module_dir: str, module_name: str, provider_config: DictConfig):
    outputs = provider_config.outputs
    tf_outputs_template = env.get_template("outputs.tf")
    tf_outputs_file_path = f"{module_dir}/outputs.tf"
    log.info(f"Generating terraform template: {tf_outputs_file_path}")

    with open(tf_outputs_file_path, 'w') as tf_outputs_file:
        tf_outputs_file.write(tf_outputs_template.render(module_name=module_name,
                                                         outputs=outputs))



def build_templates(module_name: str, provider_name: str, infra: DictConfig):

    provider_config = infra.providers[provider_name]
    infra_config = infra.config

    log.debug(f"provider_config: {provider_config}")
    log.debug(f"infra_config: {infra_config}")

    module_dir = f"{provider_config.module_path}/{module_name}"
    os.makedirs(module_dir, exist_ok=True)

    generate_terraform_config_file(module_dir, module_name, provider_config)
    generate_terraform_module(module_dir, module_name, infra_config.copy(), provider_config)
    generate_terraform_outputs(module_dir, module_name, provider_config)



def generate_terraform_module(module_dir: str, module_name: str, module_config: DictConfig, provider_config: DictConfig):
    tags = module_config.tags
    del module_config.tags  # Remove tags from dictionary so template doesn't render them incorrectly

    tf_module_file_path = f"{module_dir}/{module_name}.tf"
    log.info(f"Generating terraform template: {tf_module_file_path}")

    with open(tf_module_file_path, 'w') as tf_module_file:
        tf_module_file.write(tf_module_template.render(module_name=module_name,
                                                       module_config=module_config,
                                                       module_url=provider_config.module_url,
                                                       module_source=provider_config.module_source,
                                                       module_version=provider_config.module_version,
                                                       tags=tags))


def generate_terraform_config_file(module_dir: str, module_name: str, provider_config: DictConfig):
    tf_config_template = env.get_template("terraform_config.tf")
    tf_config_file_path = f"{module_dir}/terraform_config.tf"
    log.info(f"Generating terraform template: {tf_config_file_path}")

    s3_backend_key = f"{provider_config.s3_backend_root}/{module_name}"
    with open(tf_config_file_path, 'w') as tf_config_file:
        tf_config_file.write(tf_config_template.render(s3_backend_key=s3_backend_key))
