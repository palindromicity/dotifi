from dotifi.configuration.load import load_configuration
import pathlib

SAMPLE = pathlib.Path(__file__).parent.parent.joinpath("configurations/sample.yml")
NO_ENV = pathlib.Path(__file__).parent.joinpath("resources/env.yml")


def test_load_sample_configuration():
    configuration = load_configuration({}, SAMPLE.absolute().as_posix())
    assert configuration is not None


def test_load_env_configuration():
    configuration = load_configuration({}, NO_ENV.absolute().as_posix())
    assert configuration["path"].as_str_expanded() != "${PATH}"
    assert configuration["not_path"].get() == "not path"
