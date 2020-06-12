import logging
import os.path

from confuse import LazyConfig


def load_configuration(args, configuration_file_path) -> LazyConfig:
    config = LazyConfig("Service", __name__)
    if configuration_file_path is not None:
        logging.debug("configuration file path is %s", config)
        if os.path.isfile(configuration_file_path):
            config_file = configuration_file_path
            config.set_file(config_file)
            print("Loaded configuration from %s", configuration_file_path)
        else:
            raise Exception("%s is not a file", configuration_file_path)
    config.set_args(args)
    return config
