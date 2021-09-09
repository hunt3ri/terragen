from hydra import initialize, compose
from providers.aws.terragen.app.build_templates import build_templates


def test_vpc_config():
    with initialize(config_path="../../../../config"):
        cfg = compose(config_name="atlas")
        vpc_config = cfg.aws.shared.vpc
