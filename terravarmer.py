import hydra

from app.connectivity import create_sg_rules
from app.terraform import create_infrastructure, destroy_infrastructure
from omegaconf import DictConfig

from providers.cloud_provider import CloudProvider


@hydra.main(config_path="./config", config_name="atlas")
def terravarmer(cfg: DictConfig) -> None:
    """ Parse config and create or destroy AWS infrastructure """
    cloud_provider = CloudProvider().build_provider("AWSTerraformProvider")
    cloud_provider.create_shared_infra(cfg)


    #
    # if terraform_mode == "ccreate":
    #     create_infrastructure(cfg)
    #     if cfg.build.apply_connectivity_rules:
    #         create_sg_rules(cfg.build.use_local_aws_creds, cfg.connectivity)  # Applies additional SG rules to infra
    # elif terraform_mode == "destroy":
    #     destroy_infrastructure(cfg)


if __name__ == "__main__":
    terravarmer()
