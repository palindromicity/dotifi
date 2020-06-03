import pathlib

import jsonpickle
import pytest
from pygraphviz import AGraph

from dotifi.configuration.load import load_configuration
from dotifi.nifi.generate import generate_graph

MOCK_DATA = pathlib.Path(__file__).parent.parent.parent.joinpath("resources/test_mock_data.pickle")
SAMPLE_GRAPH = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("sample_output/nifi-canvas.dot")


@pytest.fixture
def args(mocker):
    # setup mocking for nipyapi
    pickled = MOCK_DATA.read_text()
    mock_data = jsonpickle.decode(pickled)
    assert mock_data is not None
    assert len(mock_data) > 0

    # when running from dotifi must patch dotifi.

    root_pg = mocker.patch("dotifi.nifi.generate.nipyapi.canvas.get_root_pg_id")
    root_pg.return_value = mock_data['nipyapi.canvas.get_root_pg_id']['return']

    process_groups_api = mocker.patch("dotifi.nifi.generate.nipyapi.nifi.apis.process_groups_api")
    process_groups_api.return_value = mock_data['nipyapi.nifi.ProcessGroupsApi']['return']

    process_groups_api_get_process_groups = mocker.patch(
        "dotifi.nifi.generate.nipyapi.nifi.apis.process_groups_api.get_process_groups")

    def get_pgs_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if key.startswith('ProcessGroupsApi.get_process_groups') and value['args'][0] == args[0]:
                return value['return']
        return None

    process_groups_api_get_process_groups.side_effect = get_pgs_sides

    process_groups_api_get_process_groupsd = mocker.patch(
        "dotifi.nifi.generate.nipyapi.nifi.apis.ProcessGroupsApi.get_process_groups")
    process_groups_api_get_process_groupsd.side_effect = get_pgs_sides

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

    canvas_list_input_ports = mocker.patch("dotifi.nifi.generate.nipyapi.canvas.list_all_input_ports")

    def get_list_all_input_ports_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if len(args) == len(value['args']):
                if key.startswith('nipyapi.canvas.list_all_input_ports'):
                    for i in range(len(args)):
                        if value['args'][0] == args[0]:
                            return value['return']
        return None

    canvas_list_input_ports.side_effect = get_list_all_input_ports_sides

    canvas_list_output_ports = mocker.patch("dotifi.nifi.generate.nipyapi.canvas.list_all_output_ports")

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
    canvas_get_rpg = mocker.patch("dotifi.nifi.generate.nipyapi.canvas.get_remote_process_group")

    def get_rpg_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if key.startswith('nipyapi.canvas.get_remote_process_group'):
                for i in range(len(args)):
                    if value['args'][0] == args[0]:
                        return value['return']
        return None

    canvas_get_rpg.side_effect = get_rpg_sides
    return {"output_dot_file": "nifi_canvas", "output_graphviz_format": "png", "output_graphviz_program": "dot",
            "output_graphviz_file": "nifi_canvas", "depth": -1, "nifi_url": "http://localhost:8080/nifi_api",
            "verbose": False, "generate_mock_data": False, "mock_data_file": "mock_output.json"}


def test_happy_path(args):
    """
    Test the basic setup of our mocking
    This function loads our pickled results from live
    calls, and mocks the calls and returns to the parameters,
    which are mainly uuid strings
    :param args the args fixture
    """

    options = load_configuration(args, None)

    graph = generate_graph(options)
    base_graph = AGraph(SAMPLE_GRAPH.as_posix())
    assert graph is not None
    assert graph.number_of_edges() == base_graph.number_of_edges()
    assert graph.number_of_nodes() == base_graph.number_of_nodes()
    assert sorted(dict(graph.edges())) == sorted(dict(base_graph.edges()))
    assert sorted(graph.nodes()) == sorted(base_graph.nodes())
