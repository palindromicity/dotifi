import jsonpickle
import pytest


@pytest.fixture
def mock_data(path_arg):
    pickled = path_arg.read_text()
    mock_data = jsonpickle.decode(pickled)
    assert mock_data is not None
    assert len(mock_data) > 0
    return mock_data


@pytest.fixture
def mock_setup(mocker, mock_data):

    # when running from dotifi must patch dotifi.

    if mock_data.get("nipyapi.canvas.get_root_pg_id") is not None:
        root_pg = mocker.patch("dotifi.nifi.generate.nipyapi.canvas.get_root_pg_id")
        root_pg.return_value = mock_data["nipyapi.canvas.get_root_pg_id"]["return"]

    get_process_group = mocker.patch(
        "dotifi.nifi.generate.nipyapi.canvas.get_process_group"
    )

    def get_pg_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if (
                key.startswith("nipyapi.canvas.get_process_group")
                and value["args"][0] == args[0]
            ):
                return value["return"]
        return None

    get_process_group.side_effect = get_pg_sides

    process_groups_api = mocker.patch(
        "dotifi.nifi.generate.nipyapi.nifi.apis.process_groups_api"
    )
    process_groups_api.return_value = mock_data["nipyapi.nifi.ProcessGroupsApi"][
        "return"
    ]

    process_groups_api_get_process_groups = mocker.patch(
        "dotifi.nifi.generate.nipyapi.nifi.apis.process_groups_api.get_process_groups"
    )

    def get_pgs_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if (
                key.startswith("ProcessGroupsApi.get_process_groups")
                and value["args"][0] == args[0]
            ):
                return value["return"]
        return None

    process_groups_api_get_process_groups.side_effect = get_pgs_sides

    process_groups_api_get_process_groupsd = mocker.patch(
        "dotifi.nifi.generate.nipyapi.nifi.apis.ProcessGroupsApi.get_process_groups"
    )
    process_groups_api_get_process_groupsd.side_effect = get_pgs_sides

    canvas_get_flow = mocker.patch("nipyapi.canvas.get_flow")

    def get_flow_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if len(args) == len(value["args"]):
                if key.startswith("nipyapi.canvas.get_flow"):
                    for i in range(len(args)):
                        if value["args"][0] == args[0]:
                            return value["return"]
        return None

    canvas_get_flow.side_effect = get_flow_sides

    canvas_list_input_ports = mocker.patch(
        "dotifi.nifi.generate.nipyapi.canvas.list_all_input_ports"
    )

    def get_list_all_input_ports_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if len(args) == len(value["args"]):
                if key.startswith("nipyapi.canvas.list_all_input_ports"):
                    for i in range(len(args)):
                        if value["args"][0] == args[0]:
                            return value["return"]
        return None

    canvas_list_input_ports.side_effect = get_list_all_input_ports_sides

    canvas_list_output_ports = mocker.patch(
        "dotifi.nifi.generate.nipyapi.canvas.list_all_output_ports"
    )

    def get_list_all_output_ports_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if len(args) == len(value["args"]):
                if key.startswith("nipyapi.canvas.list_all_output_ports"):
                    for i in range(len(args)):
                        if value["args"][0] == args[0]:
                            return value["return"]
        return None

    canvas_list_output_ports.side_effect = get_list_all_output_ports_sides

    # nipyapi.canvas.get_remote_process_group
    canvas_get_rpg = mocker.patch(
        "dotifi.nifi.generate.nipyapi.canvas.get_remote_process_group"
    )

    def get_rpg_sides(*args, **kwargs):
        for key, value in mock_data.items():
            if key.startswith("nipyapi.canvas.get_remote_process_group"):
                for i in range(len(args)):
                    if value["args"][0] == args[0]:
                        return value["return"]
        return None

    canvas_get_rpg.side_effect = get_rpg_sides


@pytest.fixture
def default_args(mock_setup):
    return {
        "output_dot_file": "nifi_canvas",
        "output_graphviz_format": "png",
        "output_graphviz_program": "dot",
        "output_graphviz_file": "nifi_canvas",
        "depth": -1,
        "nifi_url": "http://localhost:8080/nifi_api",
        "verbose": False,
        "generate_mock_data": False,
        "mock_data_file": "mock_output.json",
    }


@pytest.fixture
def pg_start_args(mock_setup):
    return {
        "start_at_pg": "351dbb56-0172-1000-21fa-a4af9fc0dbb1",
        "output_dot_file": "nifi_canvas",
        "output_graphviz_format": "png",
        "output_graphviz_program": "dot",
        "output_graphviz_file": "nifi_canvas",
        "depth": -1,
        "nifi_url": "http://localhost:8080/nifi_api",
        "verbose": False,
        "generate_mock_data": False,
        "mock_data_file": "mock_output.json",
    }
