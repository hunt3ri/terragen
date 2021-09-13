import logging
import os
from omegaconf import DictConfig

log = logging.getLogger(__name__)


def build_templates(module_name: str, provider_name: str, infra: DictConfig):

    provider_config = infra.providers[provider_name]
    infra_config = infra.config

    log.debug(f"provider_config: {provider_config}")
    log.debug(f"infra_config: {infra_config}")
    iain = provider_config.module_path

    module_dir = f"{provider_config.module_path}/{module_name}"

    os.makedirs(module_dir, exist_ok=True)

    # Write File

    # for config_key in infra.config:
    #     test = infra.config[config_key]
    #     iain = test
