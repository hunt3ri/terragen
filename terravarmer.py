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

    build_config = cfg.build
    shared_config = cfg.shared

    for service, service_configs in shared_config.items():
        for infra_name, infra_config in service_configs.items():
            cloud_provider = CloudProvider.from_build_config(infra_config.providers.default_provider, build_config)
            cloud_provider.create_shared_infra(service, infra_name, infra_config)


if __name__ == "__main__":
    terravarmer()
