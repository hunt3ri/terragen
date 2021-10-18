import hydra
import logging

from omegaconf import DictConfig
from providers.cloud_provider import CloudProvider

log = logging.getLogger(__name__)


@hydra.main(config_path="./config", config_name="atlas")
def terravarmer(cfg: DictConfig) -> None:
    """ Parse config and create or destroy AWS infrastructure """
    log.info("TerraVarmer starting up")

    if "shared" in cfg.keys():
        process_shared_infra(cfg)


def process_shared_infra(cfg: DictConfig):
    log.info("TerraVarmer processing shared infrastructure")
    build_config = cfg.build
    shared_config = cfg.shared

    shared_config_items = shared_config.items()
    if build_config.shared_infra == "destroy":
        # If destroying we want to do it in reverse order from creation
        shared_config_items = reversed(shared_config.items())

    for service, service_configs in shared_config_items:
        for infra_name, infra_config in service_configs.items():
            cloud_provider = CloudProvider.from_build_config(infra_config.providers.default_provider, build_config)

            if build_config.shared_infra == "create":
                cloud_provider.create_shared_infra(service, infra_name, infra_config)
            elif build_config.shared_infra == "destroy":
                cloud_provider.destroy_shared_infra(service, infra_name, infra_config)


if __name__ == "__main__":
    terravarmer()
