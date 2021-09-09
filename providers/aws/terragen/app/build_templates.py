from omegaconf import DictConfig


def build_templates(infra: DictConfig, provider_name: str):

    provider_config = infra.providers[provider_name]

    for config_key in infra.configs:
        infra = infra.configs[config_key]
        iain = infra
