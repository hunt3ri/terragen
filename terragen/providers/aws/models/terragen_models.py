import attr
from omegaconf import DictConfig
from omegaconf.errors import ConfigAttributeError


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
