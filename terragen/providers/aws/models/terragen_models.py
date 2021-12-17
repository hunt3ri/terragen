import attr
from omegaconf import DictConfig
from omegaconf.errors import ConfigAttributeError


# @attr.s
# class TerraformBackend:
#     bucket: str = attr.ib()
#     region: str = attr.ib()
#     profile: str = attr.ib()
#     state_file: str = attr.ib(default="set me later")
#
#     @classmethod
#     def from_hydra_config(cls, bucket: str, region: str, profile: str):
#         return cls(bucket=bucket, region=region, profile=profile)
#
#     @classmethod


@attr.s
class AWSEnvironment:
    """ This class models Environment specific config """
    bucket: str = attr.ib()
    region: str = attr.ib()
    profile: str = attr.ib()
    state_file: str = attr.ib(default="set me later")

    @classmethod
    def from_environment_config(cls, env_config: DictConfig):
        try:
            bucket = env_config.bucket
            region = env_config.region
            profile = env_config.profile
        except ConfigAttributeError as e:
            raise ValueError(f"Missing mandatory value in Environment config: {e.msg}")

        return cls(
            bucket=bucket,
            region=region,
            profile=profile
        )


@attr.s
class TerragenProperties:
    debug_mode: bool = attr.ib()
    environment: str = attr.ib()
    provider_name: str = attr.ib()
    aws_environment: AWSEnvironment = attr.ib()
    terraform_plan: bool = attr.ib(default=False)

    @classmethod
    def from_properties(cls, debug_mode: bool, environment: str, provider_name: str, terraform_mode: str, aws_environment: AWSEnvironment):

        if terraform_mode == "plan":
            terraform_plan = True

        return cls(
            debug_mode=debug_mode,
            environment=environment,
            provider_name=provider_name,
            terraform_plan=terraform_plan,
            aws_environment=aws_environment
        )
