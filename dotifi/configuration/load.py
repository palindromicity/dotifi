import logging
import os.path

from confuse import LazyConfig


def load_configuration(args, configuration_file_path) -> LazyConfig:
    config = LazyConfig("Service", __name__)
    if configuration_file_path is not None:
        logging.debug(f"configuration file path is {configuration_file_path}")
        if os.path.isfile(configuration_file_path):
            config_file = configuration_file_path
            config.set_file(config_file)
            print(f"Loaded configuration from {configuration_file_path}")
        else:
            raise Exception(f"{configuration_file_path} is not a file")
    config.set_args(args)
    return config
