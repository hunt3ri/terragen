import attr
import os
from omegaconf import DictConfig
from omegaconf.errors import ConfigAttributeError
from pathlib import Path

from terragen.providers.cloud_provider import BuildConfig


@attr.s
class AWSEnvironment:
    """ This class models Environment specific config """
    bucket: str = attr.ib()
    region: str = attr.ib()
    profile: str = attr.ib()
    state_file: str = attr.ib(default="set me later")

    @classmethod
    def from_environment_config(cls, env_config: DictConfig, module_metadata: DictConfig):
        try:
            bucket = env_config.bucket
            region = env_config.region
            profile = env_config.profile
        except ConfigAttributeError as e:
            raise ValueError(f"Missing mandatory value in Environment config: {e.msg}")

        return cls(
            bucket=bucket,
            region=region,
            profile=profile,
            state_file=module_metadata.state_file
        )


@attr.s
class AWSModule:
    module_name: str = attr.ib()
    hydra_dir: str = attr.ib()  # The Hydra output dir
    module_config: DictConfig = attr.ib()
    module_metadata: DictConfig = attr.ib()
    service_name: str = attr.ib()
    tfvars_file: str = attr.ib()
    lookups: DictConfig = attr.ib()

    @classmethod
    def from_config(cls, module_config: DictConfig, build_config: BuildConfig):
        module_metadata = module_config.module_metadata
        module_name = module_metadata.name
        service_name = module_metadata.aws_service

        # Create path for outputting tf modules within hydra output dir
        hydra_dir = Path(
            f"{os.getcwd()}/{build_config.cloud_provider}/{build_config.environment}/{service_name}/{module_name}"
        )

        return cls(
            module_name=module_name,
            module_config=module_config.config,
            service_name=service_name,
            hydra_dir=str(hydra_dir),
            module_metadata=module_metadata,
            tfvars_file=f"{module_name}.tfvars",
            lookups=module_config.lookups,
        )
