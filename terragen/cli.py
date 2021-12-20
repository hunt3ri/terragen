import hydra
import logging
import sys

from omegaconf import DictConfig, OmegaConf
from omegaconf.errors import MissingMandatoryValue, InterpolationKeyError
from terragen.providers.cloud_provider import CloudProvider, BuildConfig

log = logging.getLogger(__name__)


def entrypoint() -> None:
    """Entrypoint for terragen cli"""
    try:
        build_infra()
    except InterpolationKeyError as error:
        log.error(f"Config Error: {error}")
        sys.exit(1)


@hydra.main(config_path="../config", config_name="config")
def build_infra(cfg: DictConfig):
    log.info("Terragen starting up")
    if not is_valid_config(cfg):
        sys.exit(1)  # Invalid config so immediately stop processing

    build_config = BuildConfig.from_build_config_yaml(cfg.build)

    if build_config.infra_shared == "destroy" and build_config.infra_app == "destroy":
        # If we're destroying the entire stack destroy app specific infra ahead of shared infra
        if "app" in cfg:
            process_infra(build_config, cfg.app, build_config.infra_app, cfg.environment)
        if "shared" in cfg:
            process_infra(build_config, cfg.shared, build_config.shared_infra, cfg.environment)
    else:
        # for all other scenarios we want to process shared infra ahead of app specific infra
        if "shared" in cfg:
            process_infra(build_config, cfg.shared, build_config.infra_shared, cfg.environment)
        if "app" in cfg:
            process_infra(build_config, cfg.app, build_config.infra_app, cfg.environment)


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


def process_infra(build_config: BuildConfig, cloud_config: DictConfig, mode: str, env_config: DictConfig):
    log.info(f"TerraGen processing infrastructure with mode: {mode}")

    if mode == "pass":
        log.info("Infrastructure mode is pass, so skipping updating infrastructure")
        return

    terraform_modules = cloud_config.items()
    if mode == "destroy":
        # If destroying we want to do it in reverse order from creation
        terraform_modules = reversed(cloud_config.items())

    cloud_provider = CloudProvider.from_config(build_config, env_config)
    for service, module_configs in terraform_modules:
        for module_name, module_config in module_configs.items():
            if mode == "create":
                cloud_provider.create_infra(module_config)
            elif mode == "destroy":
                cloud_provider.destroy_infra(module_config)


if __name__ == "__main__":
    try:
        entrypoint()
    except InterpolationKeyError as e:
        log.error(f"Config Error: {e}")
        exit(1)
