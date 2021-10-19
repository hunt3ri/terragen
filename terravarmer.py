import hydra
import logging

from omegaconf import DictConfig
from providers.cloud_provider import CloudProvider

log = logging.getLogger(__name__)


@hydra.main(config_path="./config", config_name="atlas")
def terravarmer(cfg: DictConfig) -> None:
    """ Parse config and create or destroy AWS infrastructure """
    log.info("TerraVarmer starting up")

    build_config = cfg.build

    if "shared" in cfg.keys():
        pass
        # process_infra(build_config, cfg.shared, build_config.shared_infra)

    if "app" in cfg.keys():
        process_infra(build_config, cfg.app, build_config.app_infra)


def process_infra(build_config: DictConfig, infra_config: DictConfig, mode: str):
    log.info(f"TerraVarmer processing infrastructure with mode: {mode}")

    config_items = infra_config.items()
    if mode == "destroy":
        # If destroying we want to do it in reverse order from creation
        config_items = reversed(infra_config.items())

    for service, service_configs in config_items:
        for infra_name, infra_config in service_configs.items():
            cloud_provider = CloudProvider.from_build_config(infra_config.providers.default_provider, build_config)

            if mode == "create":
                cloud_provider.create_infra(service, infra_name, infra_config)
            elif mode == "destroy":
                cloud_provider.destroy_infra(service, infra_name, infra_config)


if __name__ == "__main__":
    terravarmer()
