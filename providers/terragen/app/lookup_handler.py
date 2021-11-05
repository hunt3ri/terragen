import attr
import logging

from dataclasses import dataclass, field
from omegaconf import DictConfig, ListConfig, OmegaConf
from typing import List

log = logging.getLogger(__name__)


@dataclass
class TempList:
    lookups: List[str] = field(default_factory=lambda: [])


@attr.s
class LookupHandler:

    module_name: str = attr.ib()
    module_config: DictConfig = attr.ib()
    datablock_keys: [] = attr.ib()

    @classmethod
    def from_module_config(cls, module_name: str, module_config: DictConfig):
        return cls(module_name=module_name, module_config=module_config, datablock_keys=[])

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
                    datablock_key, datablock_lookup = self.get_lookup_values(lookup)
                    temp_list.lookups.append(f"data.terraform_remote_state.{self.module_name}.{datablock_lookup}")
                    self.datablock_keys.append(datablock_key)
                else:
                    temp_list.lookups.append(lookup)

            self.module_config[key] = temp_list.lookups
        elif "lookup" in value:
            datablock_key, datablock_lookup = self.get_lookup_values(value)
            self.module_config[key] = f"data.terraform_remote_state.{self.module_name}.{datablock_lookup}"
            self.datablock_keys.append(datablock_key)

    def get_lookup_values(self, lookup: str):
        """ Remove all Hydra lookup text to allow us to reinsert a Terraform compatible data block lookup """
        clean_lookup = lookup.replace("lookup:", "").strip()
        lookup_array = clean_lookup.split('.outputs')

        if len(lookup_array) != 2:
            raise ValueError(f"Supplied lookup {lookup} does not contain .outputs")

        datablock_key = lookup_array[0].replace(".", "/")
        datablock_lookup = f"outputs{lookup_array[1]}"

        # TODO create a datablock model, use this value to uniquely identify blocks
        unique = datablock_key.rsplit('/', 1)[1]

        return datablock_key, datablock_lookup
