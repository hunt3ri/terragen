import attr
import textwrap
from omegaconf import DictConfig


@attr.s
class TerraformAWSProvider:
    region: str = attr.ib()
    profile: str = attr.ib()

    @classmethod
    def from_hydra_config(cls, provider_config: DictConfig):
        return cls(region=provider_config.region,
                   profile=provider_config.profile)

    def __str__(self):
        return textwrap.dedent(f"""
            provider "aws" {{
                region  = "{self.region}"  
                profile = "{self.profile}"
            }}   
            """)


@attr.s
class TerraformS3Backend:
    bucket: str = attr.ib()
    region: str = attr.ib()
    profile: str = attr.ib()
    key: str = attr.ib(default="set me later")

    @classmethod
    def from_hydra_config(cls, backend_config: DictConfig):
        return cls(bucket=backend_config.bucket,
                   region=backend_config.region,
                   profile=backend_config.profile)

    def __str__(self):
        return textwrap.dedent(f"""
            backend "s3" {{
                profile = "{self.profile}"
                region  = "{self.region}"
                bucket  = "{self.bucket}" 
                key     = "{self.key}"
            }}
            """
        )


@attr.s
class TerragenProperties:
    debug_mode: bool = attr.ib()
    environment: str = attr.ib()
    run_terraform: bool = attr.ib()
    terraform_mode: str = attr.ib()
    provider = attr.ib()
    backend = attr.ib()
    provider_name: str = attr.ib()

    @terraform_mode.validator
    def validate_terraform_mode(self, attribute, value):
        assert value in ["create", "destroy", "plan"]

    @classmethod
    def from_properties(cls, debug_mode: bool, environment: str, provider_name: str, provider_properties: DictConfig):
        backend_config = provider_properties.backend_config
        provider_config = provider_properties.provider_config

        if backend_config.terraform_backend == "S3":
            backend = TerraformS3Backend.from_hydra_config(backend_config)
        else:
            raise ValueError(f"{backend_config.terraform_backend} backend currently unsupported")

        if provider_config.terraform_provider == "AWS":
            provider = TerraformAWSProvider.from_hydra_config(provider_config)
        else:
            raise ValueError(f"{provider_config.terraform_provider} provider currently unsupported")

        return cls(debug_mode=debug_mode,
                   environment=environment,
                   run_terraform=provider_properties.run_terraform,
                   terraform_mode=provider_properties.terraform_mode,
                   backend=backend,
                   provider=provider,
                   provider_name=provider_name)
