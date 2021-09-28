import attr


@attr.s
class TerragenProperties:
    run_terraform: bool = attr.ib()
    terraform_mode: str = attr.ib()
    terraform_init_cmd: str = attr.ib()

    @terraform_mode.validator
    def validate_terraform_mode(self, attribute, value):
        assert value in ["create", "destroy", "plan"]

    @classmethod
    def from_properties_bag(cls, provider_properties: dict):
        return cls(run_terraform=provider_properties["run_terraform"],
                   terraform_mode=provider_properties["terraform_mode"],
                   terraform_init_cmd=provider_properties["terraform_init_cmd"])
