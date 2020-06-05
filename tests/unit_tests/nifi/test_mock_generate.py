import pathlib

import pytest
from dotifi.configuration.load import load_configuration
from dotifi.nifi.generate import generate_graph
from pygraphviz import AGraph

HAPPY_MOCK_DATA = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "resources/test_happy_path_mock_data.pickle"
)
START_AT_MOCK_DATA = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "resources/test_mock_data_start_at_pg.pickle"
)
SAMPLE_GRAPH = pathlib.Path(__file__).parent.parent.parent.parent.joinpath(
    "sample_output/nifi-canvas.dot"
)


@pytest.mark.parametrize("path_arg", [HAPPY_MOCK_DATA])
def test_happy_path(default_args):
    """
    Test the basic setup of our mocking
    This function loads our pickled results from live
    calls, and mocks the calls and returns to the parameters,
    which are mainly uuid strings
    :param args the args fixture
    """

    options = load_configuration(default_args, None)

    graph = generate_graph(options)
    base_graph = AGraph(SAMPLE_GRAPH.as_posix())
    assert graph is not None
    assert graph.number_of_edges() == base_graph.number_of_edges()
    assert graph.number_of_nodes() == base_graph.number_of_nodes()
    assert sorted(dict(graph.edges())) == sorted(dict(base_graph.edges()))
    assert sorted(graph.nodes()) == sorted(base_graph.nodes())


@pytest.mark.parametrize("path_arg", [START_AT_MOCK_DATA])
def test_start_pg(pg_start_args):
    """
        Test the basic setup of our mocking
        This function loads our pickled results from live
        calls, and mocks the calls and returns to the parameters,
        which are mainly uuid strings
        :param args the args fixture
        """

    options = load_configuration(pg_start_args, None)

    graph = generate_graph(options)
    assert graph is not None
    assert graph.graph_attr["id"] == pg_start_args["start_at_pg"]
    from dotifi.publishing.publish import publish

    publish(options, graph)
