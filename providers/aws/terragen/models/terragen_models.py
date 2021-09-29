import textwrap

import attr


@attr.s
class TerraformAWSProvider:
    region: str = attr.ib()
    profile: str = attr.ib()

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
    key: str = attr.ib()

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
    run_terraform: bool = attr.ib()
    terraform_mode: str = attr.ib()
    terraform_init_cmd: str = attr.ib()
    provider = TerraformAWSProvider = attr.ib()
    backend = TerraformS3Backend = attr.ib()

    @terraform_mode.validator
    def validate_terraform_mode(self, attribute, value):
        assert value in ["create", "destroy", "plan"]

    @classmethod
    def from_properties_bag(cls, provider_properties: dict):
        return cls(run_terraform=provider_properties["run_terraform"],
                   terraform_mode=provider_properties["terraform_mode"],
                   terraform_init_cmd=provider_properties["terraform_init_cmd"])
