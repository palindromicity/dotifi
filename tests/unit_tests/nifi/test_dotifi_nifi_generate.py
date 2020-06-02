import pathlib

import jsonpickle
import nipyapi

SAMPLE = pathlib.Path(__file__).parent.parent.joinpath("configurations/sample.yml")
NO_ENV = pathlib.Path(__file__).parent.joinpath("resources/env.yml")

MOCK_DATA = pathlib.Path(__file__).parent.parent.parent.joinpath("resources/test_mock_data.pickle")


def test_mechanics(mocker):
    """
    Test the basic setup of our mocking
    This function loads our pickled results from live
    calls, and mocks the calls and returns to the parameters,
    which are mainly uuid strings
    :param mocker: the pytest-mock mocker
    """
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

    canvas_get_flow = mocker.patch("nipyapi.canvas.get_flow")

    def get_flow_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if len(args) == len(value['args']):
                if key.startswith('nipyapi.canvas.get_flow'):
                    for i in range(len(args)):
                        if value['args'][0] == args[0]:
                            return value['return']
        return None

    canvas_get_flow.side_effect = get_flow_sides

    canvas_list_input_ports = mocker.patch("nipyapi.canvas.list_all_input_ports")

    def get_list_all_input_ports_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if len(args) == len(value['args']):
                if key.startswith('nipyapi.canvas.list_all_input_ports'):
                    for i in range(len(args)):
                        if value['args'][0] == args[0]:
                            return value['return']
        return None

    canvas_list_input_ports.side_effect = get_list_all_input_ports_sides

    canvas_list_output_ports = mocker.patch("nipyapi.canvas.list_all_output_ports")

    def get_list_all_output_ports_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if len(args) == len(value['args']):
                if key.startswith('nipyapi.canvas.list_all_output_ports'):
                    for i in range(len(args)):
                        if value['args'][0] == args[0]:
                            return value['return']
        return None

    canvas_list_output_ports.side_effect = get_list_all_output_ports_sides

    # nipyapi.canvas.get_remote_process_group
    canvas_get_rpg = mocker.patch("nipyapi.canvas.get_remote_process_group")

    def get_rpg_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if len(args) == len(value['args']):
                if key.startswith('nipyapi.canvas.get_remote_process_group'):
                    for i in range(len(args)):
                        if value['args'][0] == args[0]:
                            return value['return']
        return None

    canvas_get_rpg.side_effect = get_rpg_sides

    response = nipyapi.nifi.ProcessGroupsApi()
    assert type(response) == type(mock_data['nipyapi.nifi.ProcessGroupsApi']['return'])

    for key, value in mock_data.items():
        if key.startswith('ProcessGroupsApi.get_process_groups'):
            this_response = nipyapi.nifi.ProcessGroupsApi().get_process_groups(value['args'][0])
            i = 0
            for pg in this_response.process_groups:
                assert pg.id == value['return'][i].id
                assert this_response.process_groups[i].id == value['return'][i].id
                i = i + 1
        if key.startswith("nipyapi.canvas.get_flow"):
            this_response = nipyapi.canvas.get_flow(value['args'][0])
            assert this_response.process_group_flow.id == value['return'].process_group_flow.id
        if key.startswith("nipyapi.canvas.get_remote_process_group"):
            this_response = nipyapi.canvas.get_remote_process_group(value['args'][0])
            if this_response is not None:
                assert this_response.remote_process_group.id == value['return'].remote_process_group.id
        if key.startswith('nipyapi.canvas.list_all_input_ports'):
            this_response = nipyapi.canvas.list_all_input_ports(value['args'][0])
            i = 0
            if this_response is not None:
                for ip in this_response:
                    assert ip.id == value['return'][i].id
                    assert this_response[i].id == value['return'][i].id
                    i = i + 1
        if key.startswith('nipyapi.canvas.list_all_output_ports'):
            this_response = nipyapi.canvas.list_all_output_ports(value['args'][0])
            i = 0
            if this_response is not None:
                for ip in this_response:
                    assert ip.id == value['return'][i].id
                    assert this_response[i].id == value['return'][i].id
                    i = i + 1
