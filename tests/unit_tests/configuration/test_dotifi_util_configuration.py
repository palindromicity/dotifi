import pathlib

from dotifi.configuration.load import load_configuration

SAMPLE = pathlib.Path(__file__).parent.parent.parent.parent.joinpath(
    "configurations/sample.yaml"
)
NO_ENV = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "resources/configurations/env.yaml"
)


def test_load_sample_configuration():
    configuration = load_configuration({}, SAMPLE.absolute().as_posix())
    assert configuration is not None


def test_load_env_configuration():
    configuration = load_configuration({}, NO_ENV.absolute().as_posix())
    assert configuration["path"].as_str_expanded() != "${PATH}"
    assert configuration["not_path"].get() == "not path"
