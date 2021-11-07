import hydra
import logging

from omegaconf import DictConfig
from providers.cloud_provider import CloudProvider

log = logging.getLogger(__name__)


@hydra.main(config_path="./config", config_name="atlas")
def terragen(cfg: DictConfig) -> None:
    """ Parse config and create or destroy infrastructure """
    log.info("Terragen starting up")

    build_config = cfg.build

    if build_config.shared_infra.lower() == "destroy" and build_config.app_infra.lower() == "destroy":
        # If we're destroying the entire stack destroy app ahead of shared
        process_infra(build_config, cfg.app, build_config.app_infra)
        process_infra(build_config, cfg.shared, build_config.shared_infra)
    else:
        # for all other scenarios we want to process shared ahead of app
        process_infra(build_config, cfg.shared, build_config.shared_infra)
        process_infra(build_config, cfg.app, build_config.app_infra)


def process_infra(build_config: DictConfig, infra_config: DictConfig, mode: str):
    log.info(f"TerraGen processing infrastructure with mode: {mode}")

    if mode == "pass":
        log.info(f"Infrastructure mode is pass, so skipping updating infrastructure")
        return

    config_items = infra_config.items()
    if mode == "destroy":
        # If destroying we want to do it in reverse order from creation
        config_items = reversed(infra_config.items())

    for service, service_configs in config_items:
        for infra_name, infra_config in service_configs.items():
            cloud_provider = CloudProvider.from_build_config(infra_config.providers.default_provider, build_config)

            if mode == "create":
                cloud_provider.create_infra(infra_config)
            elif mode == "destroy":
                cloud_provider.destroy_infra(infra_config)


if __name__ == "__main__":
    terragen()
