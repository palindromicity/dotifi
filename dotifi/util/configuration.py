import yaml
import re
import os

_path_matcher = re.compile(r'\$\{([^}^{]+)\}')


def _path_constructor(loader, node):
    """ Extract the matched value, expand env variable, and replace the match """
    value = node.value
    match = _path_matcher.match(value)
    env_var = match.group()[2:-1]
    return os.environ.get(env_var) + value[match.end():]


yaml.add_implicit_resolver('!path', _path_matcher)
yaml.add_constructor('!path', _path_constructor)


def load_configuration(configuration_file_path):
    with open(configuration_file_path) as f:
        return yaml.load(f, yaml.FullLoader)
