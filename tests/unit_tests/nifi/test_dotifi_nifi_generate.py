from dotifi.configuration.load import load_configuration
import pathlib
import jsonpickle
import nipyapi
from nipyapi import nifi
import mock
import pytest_mock
from pytest_mock import mocker

SAMPLE = pathlib.Path(__file__).parent.parent.joinpath("configurations/sample.yml")
NO_ENV = pathlib.Path(__file__).parent.joinpath("resources/env.yml")

MOCK_DATA = pathlib.Path(__file__).parent.parent.parent.joinpath("resources/test_mock_data.pickle")

def test_mechanics(mocker):
    # setup mocking for nipyapi
    pickled = MOCK_DATA.read_text()
    mock_data = jsonpickle.decode(pickled)
    assert mock_data is not None
    assert len(mock_data) > 0

    # when running from dotifi must patch dotifi.
    process_groups_api = mocker.patch("nipyapi.nifi.apis.process_groups_api")
    process_groups_api.return_value = mock_data['nipyapi.nifi.ProcessGroupsApi']['return']


    process_groups_api_get_process_groups = mocker.patch("nipyapi.nifi.apis.process_groups_api.get_process_groups")

    def get_pgs_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if key.startswith('ProcessGroupsApi.get_process_groups') and value['args'][0] == args[0]:
                return value['return']
        return None
    process_groups_api_get_process_groups.side_effect = get_pgs_sides


    response = nipyapi.nifi.ProcessGroupsApi()
    assert type(response) == type(mock_data['nipyapi.nifi.ProcessGroupsApi']['return'])

    for key, value in mock_data.items():
        if key.startswith('ProcessGroupsApi.get_process_groups'):
            this_response = nipyapi.nifi.ProcessGroupsApi().get_process_groups(value['args'][0])
            i = 0
            for pg in this_response.process_groups:
                assert pg.id == value['return'][i].id
                assert this_response.process_groups[0].id == value['return'][0].id
                i = i + 1

