import attr
import logging
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from omegaconf import DictConfig

from providers.aws.app.utils import to_toml, split_fields_and_dicts
from providers.aws.models.terragen_models import TerragenProperties, TerraformDataSource
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