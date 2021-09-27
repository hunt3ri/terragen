import attr


@attr.s
class TerraformRunner:

    provider_properties: dict = attr.ib()

    @classmethod
    def from_config(cls, provider_properties):

        return cls(provider_properties=provider_properties)

    def create_infrastructure(self):
        # TODO check create mode is true
        pass

    def destroy_infrastructure(self):
        pass
