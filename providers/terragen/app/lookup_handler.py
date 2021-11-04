import attr
import logging

from omegaconf import DictConfig, ListConfig

log = logging.getLogger(__name__)


@attr.s
class LookupHandler:

    module_name: str = attr.ib()
    module_config: DictConfig = attr.ib()
    datablock_keys: []

    @classmethod
    def from_module_config(cls, module_name: str, module_config: DictConfig):
        return cls(module_name=module_name, module_config=module_config)

    def process_lookups(self, module_config):
        # TODO co-ordinate lookups
        for key, value in self.module_config.items():
            is_lookup, lookup_value = self.identify_lookup(value)
            if is_lookup:
                self.module_config[key] = f"data.terraform_remote_state.{self.module_name}.{lookup_value}"

    def identify_lookup(self, value):
            if isinstance(value, bool):
                return False, None, None
            elif "lookup" in value:
                get_lookup_values(lookup)

    def get_lookup_values(self, lookup: str):
        clean_lookup = lookup.replace("lookup:", "").strip()
        lookup_array = clean_lookup.split('.outputs')

        if len(lookup_array) != 2:
            raise ValueError(f"Supplied lookup {lookup} does not contain .outputs")

        datablock_key = lookup_array[0].replace(".", "/")
        datablock_lookup = f"outputs{lookup_array[1]}"

        return datablock_key, datablock_lookup

    # def lookup_handler(self):
    #     log.info(f"Handling lookups for service: {self.service_name} module: {self.module_name}")
    #     lookups = {}
    #     for key, value in self.module_config.items():
    #         if isinstance(value, bool):
    #             continue  # Bools are not iterable so skip
    #         elif isinstance(value, ListConfig):
    #             # iain = value[0]
    #             # abi = iain
    #             for lookup in value:
    #                 if "lookup" in lookup:
    #                     lookups[key] = value
    #                     # List handling needs to happen inline for multiple replacements
    #         elif "lookup" in value:
    #             lookups[key] = value
    #             # TODO parse values in Lists
    #
    #     if len(lookups) == 0:
    #         log.info(f"No lookups found in {self.module_name}.tf")
    #         return
    #
    #     for key, lookup in lookups.items():
    #         log.info(f"Processing lookup: {lookup}")
    #         datablock_key, datablock_lookup = get_lookup_values(lookup)
    #         self.generate_terraform_data_block(datablock_key)
    #         self.module_config[key] = f"data.terraform_remote_state.{self.module_name}.{datablock_lookup}"