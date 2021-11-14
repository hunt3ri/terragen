import attr
import textwrap
from omegaconf import DictConfig


# @attr.s
# class TerraformAWSProvider:
#     region: str = attr.ib()
#     profile: str = attr.ib()
#
#     @classmethod
#     def from_hydra_config(cls, provider_config: DictConfig):
#         return cls(region=provider_config.region, profile=provider_config.profile)
#
#     def __str__(self):
#         return textwrap.dedent(
#             f"""
#             provider "aws" {{
#                 region  = "{self.region}"
#                 profile = "{self.profile}"
#             }}
#             """
#         )
#
#
@attr.s
class TerraformBackend:
    bucket: str = attr.ib()
    region: str = attr.ib()
    profile: str = attr.ib()
    state_file: str = attr.ib(default="set me later")

    @classmethod
    def from_hydra_config(cls, bucket: str, region: str, profile: str):
        return cls(bucket=bucket, region=region, profile=profile)
#
#     def __str__(self):
#         """Remove all whitespace before adding a 2 space indent, to render nicely in config file"""
#         backend = textwrap.dedent(
#             f"""
#             backend "s3" {{
#                 profile = "{self.profile}"
#                 region  = "{self.region}"
#                 bucket  = "{self.bucket}"
#                 key     = "{self.key}"
#             }}
#             """
#         )
#         return textwrap.indent(backend, "  ")


@attr.s
class TerragenProperties:
    debug_mode: bool = attr.ib()
    environment: str = attr.ib()
    terraform_plan: bool = attr.ib()
    provider_name: str = attr.ib()
    backend: TerraformBackend = attr.ib()

    @classmethod
    def from_properties(cls, debug_mode: bool, environment: str, provider_name: str, provider_properties: DictConfig):
        backend = TerraformBackend.from_hydra_config(region=provider_properties.region,
                                                     profile=provider_properties.profile,
                                                     bucket=provider_properties.bucket)

        if provider_properties.terraform_mode.lower() == "plan":
            terraform_plan = True
        elif provider_properties.terraform_mode.lower() == "apply":
            terraform_plan = False
        else:
            raise ValueError(
                f"Unexpected terraform_mode value {provider_properties.terraform_mode} must be either plan or apply"
            )

        return cls(
            debug_mode=debug_mode,
            environment=environment,
            provider_name=provider_name,
            terraform_plan=terraform_plan,
            backend=backend
        )
