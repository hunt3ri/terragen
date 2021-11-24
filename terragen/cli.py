import hydra
import logging

from omegaconf import DictConfig, OmegaConf
from omegaconf.errors import MissingMandatoryValue
from terragen.providers.cloud_provider import CloudProvider

log = logging.getLogger(__name__)


@hydra.main(config_path="config", config_name="config")
def entrypoint(cfg: DictConfig) -> None:
    """Parse config and create or destroy infrastructure"""
    log.info("Terragen starting up")

    if not is_valid_config(cfg):
        return  # Invalid config so immediately stop processing

    build_config = cfg.build
    if build_config.shared_infra.lower() == "destroy" and build_config.app_infra.lower() == "destroy":
        # If we're destroying the entire stack destroy app specific infra ahead of shared infra
        if "app" in cfg:
            process_infra(build_config, cfg.app, build_config.app_infra)
        if "shared" in cfg:
            process_infra(build_config, cfg.shared, build_config.shared_infra)
    else:
        # for all other scenarios we want to process shared infra ahead of app specific infra
        if "shared" in cfg:
            process_infra(build_config, cfg.shared, build_config.shared_infra)
        if "app" in cfg:
            process_infra(build_config, cfg.app, build_config.app_infra)


def is_valid_config(cfg: DictConfig):
    """Validate the supplied config, will ensure all mandatory values have been supplied"""
    try:
        log.info("Validating Config")
        OmegaConf.to_container(cfg, resolve=True, throw_on_missing=True)
    except MissingMandatoryValue as e:
        log.error(f"Config Error: {e}")
        return False

    log.info("Config is Valid")
    return True


def process_infra(build_config: DictConfig, infra_config: DictConfig, mode: str):
    log.info(f"TerraGen processing infrastructure with mode: {mode}")

    if mode == "pass":
        log.info("Infrastructure mode is pass, so skipping updating infrastructure")
        return

    config_items = infra_config.items()
    if mode == "destroy":
        # If destroying we want to do it in reverse order from creation
        config_items = reversed(infra_config.items())

    cloud_provider = CloudProvider.from_build_config(build_config.default_provider, build_config)
    for service, service_configs in config_items:
        for infra_name, infra_config in service_configs.items():

            if mode == "create":
                cloud_provider.create_infra(infra_config)
            elif mode == "destroy":
                cloud_provider.destroy_infra(infra_config)


if __name__ == "__main__":
    entrypoint()
