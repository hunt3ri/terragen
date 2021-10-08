from hydra import initialize, compose


def test_vpc_config():
    with initialize(config_path="../../../config"):
        cfg = compose(config_name="atlas")
        vpc_config = cfg.aws.shared.vpc
