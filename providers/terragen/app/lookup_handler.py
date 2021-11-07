import attr
import logging

from dataclasses import dataclass, field
from omegaconf import DictConfig, ListConfig, OmegaConf
from typing import List
from providers.terragen.models.terragen_models import TerraformDataSource

log = logging.getLogger(__name__)


@dataclass
class TempList:
    lookups: List[str] = field(default_factory=lambda: [])


@attr.s
class LookupHandler:

    module_name: str = attr.ib()
    module_config: DictConfig = attr.ib()
    data_sources: [TerraformDataSource] = attr.ib()

    @classmethod
    def from_module_config(cls, module_name: str, module_config: DictConfig):
        return cls(module_name=module_name, module_config=module_config, data_sources=[])

    def process_lookups(self):
        for key, value in self.module_config.items():
            self.set_lookup_values(key, value)

    def set_lookup_values(self, key, value):
        if isinstance(value, bool):
            return  # Bools are not iterable so need special case
        elif isinstance(value, ListConfig):
            temp_list: TempList = OmegaConf.structured(TempList)
            for lookup in value:
                if "lookup" in lookup:
                    tf_datasource = TerraformDataSource.from_lookup(lookup)
                    temp_list.lookups.append(tf_datasource.reference)
                    self.data_sources.append(tf_datasource)
                else:
                    temp_list.lookups.append(lookup)

            self.module_config[key] = temp_list.lookups
        elif "lookup" in value:
            tf_datasource = TerraformDataSource.from_lookup(value)
            self.module_config[key] = tf_datasource.reference
            self.data_sources.append(tf_datasource)
