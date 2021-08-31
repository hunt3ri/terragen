import hydra
from app.connectivity import create_sg_rules
from app.terraform import create_infrastructure, destroy_infrastructure
from omegaconf import DictConfig


@hydra.main(config_path="./config", config_name="atlas")
def terravarmer(cfg: DictConfig) -> None:
    """ Parse config and create or destroy AWS infrastructure """
    terraform_mode = cfg.build.terraform_mode
    assert terraform_mode in ["create", "destroy"]

    if terraform_mode == "create":
        create_infrastructure(cfg)
        if cfg.build.apply_connectivity_rules:
            create_sg_rules(cfg.build.use_local_aws_creds, cfg.connectivity)  # Applies additional SG rules to infra
    elif terraform_mode == "destroy":
        destroy_infrastructure(cfg)


if __name__ == "__main__":
    terravarmer()
