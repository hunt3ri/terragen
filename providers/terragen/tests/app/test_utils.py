from providers.terragen.app.utils import to_toml


def test_to_toml_happy_path():
    assert to_toml("happy", "path") == 'happy = "path"'


def test_to_toml_handles_lookups():
    lookup_value = to_toml("lookup", "data.terraform_remote_state.local_access.outputs.vpc_id")
    assert lookup_value == "lookup = data.terraform_remote_state.local_access.outputs.vpc_id"
