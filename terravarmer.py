import hydra
import logging



# from app.connectivity import create_sg_rules
# from app.terraform import create_infrastructure, destroy_infrastructure
from omegaconf import DictConfig
from providers.cloud_provider import CloudProvider

log = logging.getLogger(__name__)


@hydra.main(config_path="./config", config_name="atlas")
def terravarmer(cfg: DictConfig) -> None:
    """ Parse config and create or destroy AWS infrastructure """
    log.info("TerraVarmer starting up")

    shared_config = cfg.shared

    for key, infra in shared_config.items():
        log.info(f"TerraVarmer instantiating {infra.providers.default_provider} provider to construct {key}")
        cloud_provider = CloudProvider().build_provider(infra.providers.default_provider)
        cloud_provider.create_shared_infra(key, infra)




    # TODO parse config and create appropriate provider for each element
    # TODO handle provider specific config
    # TODO handle build config, eg debug mode

    # TODO debug mode is a special case so can be an attribute on the base class
    # TODO provider specific config should go on base class too

    # cloud_provider = CloudProvider().build_provider("TerraGen")
    # cloud_provider.create_shared_infra(cfg.aws.shared)


    #
    # if terraform_mode == "ccreate":
    #     create_infrastructure(cfg)
    #     if cfg.build.apply_connectivity_rules:
    #         create_sg_rules(cfg.build.use_local_aws_creds, cfg.connectivity)  # Applies additional SG rules to infra
    # elif terraform_mode == "destroy":
    #     destroy_infrastructure(cfg)


def iain_test():
    # logger = logging.getLogger(__name__)
    # FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    # logging.basicConfig(format=FORMAT)
    # logger.setLevel(logging.DEBUG)
    log.debug("Test")


if __name__ == "__main__":
    terravarmer()
    #iain_test()
    #Utils().init_logging()
