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
RPG_CONFIG = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "resources/rpg_attrs.yaml"
)
PROCESSOR_CONFIG = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "resources/processor_attrs.yaml"
)


def _find_subgraph(graph: AGraph, id: str):
    found_graph = None
    for sub in graph.subgraphs():
        if sub.graph_attr["id"] == id:
            return sub
        else:
            found_graph = _find_subgraph(sub, id)
            if found_graph is not None:
                return found_graph
    return None


def _find_node(graph: AGraph, id: str):
    found_node = None
    for sub in graph.subgraphs():
        for node in sub.nodes():
            if node.attr["id"] == id:
                return node
        else:
            found_node = _find_node(sub, id)
            if found_node is not None:
                return found_node
    return None


@pytest.mark.parametrize("path_arg", [HAPPY_MOCK_DATA])
def test_happy_path(default_args):
    """
    Test the basic setup of our mocking
    This function loads our pickled results from live
    calls, and mocks the calls and returns to the parameters,
    which are mainly uuid strings
    :param default_args the default_args fixture
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
        Test outputing a subset of a canvas by specifying
        the process group to start at
        :param pg_start_args the pg_start_args fixture
        """

    options = load_configuration(pg_start_args, None)

    graph = generate_graph(options)
    assert graph is not None
    assert graph.graph_attr["id"] == pg_start_args["start_at_pg"]



@pytest.mark.parametrize("path_arg", [HAPPY_MOCK_DATA])
def test_rpg_attribute_override(default_args):
    """
    Test overriding the graph_attr of a specific remote program group
    using the yaml configuration
    :param default_args the default_args fixture
    """

    options = load_configuration(default_args, RPG_CONFIG.as_posix())

    graph = generate_graph(options)
    base_graph = AGraph(SAMPLE_GRAPH.as_posix())
    assert graph is not None
    assert graph.number_of_edges() == base_graph.number_of_edges()
    assert graph.number_of_nodes() == base_graph.number_of_nodes()
    assert sorted(dict(graph.edges())) == sorted(dict(base_graph.edges()))
    assert sorted(graph.nodes()) == sorted(base_graph.nodes())
    rpg_subgraph = _find_subgraph(graph, "65f8c7d5-0172-1000-a916-0e5562295e08")
    default_subgraph = _find_subgraph(
        base_graph, "65f8c7d5-0172-1000-a916-0e5562295e08"
    )
    assert rpg_subgraph.graph_attr["color"] == "yellow"
    assert rpg_subgraph.graph_attr["shape"] == "star"
    assert rpg_subgraph.graph_attr.get("shape") != default_subgraph.graph_attr.get(
        "shape"
    )
    assert rpg_subgraph.graph_attr.get("color") != default_subgraph.graph_attr.get(
        "color"
    )


@pytest.mark.parametrize("path_arg", [HAPPY_MOCK_DATA])
def test_processor_attribute_override(default_args):
    """
    Test overriding the attr of a specific processor
    using the yaml configuration
    :param default_args the default_args fixture
    """

    options = load_configuration(default_args, PROCESSOR_CONFIG.as_posix())

    graph = generate_graph(options)
    base_graph = AGraph(SAMPLE_GRAPH.as_posix())
    assert graph is not None
    assert graph.number_of_edges() == base_graph.number_of_edges()
    assert graph.number_of_nodes() == base_graph.number_of_nodes()
    assert sorted(dict(graph.edges())) == sorted(dict(base_graph.edges()))
    assert sorted(graph.nodes()) == sorted(base_graph.nodes())
    processor_node = _find_node(graph, "f96be8b1-78b2-42f2-6ba5-2579f4f6c411")
    default_processor_node = _find_node(
        base_graph, "f96be8b1-78b2-42f2-6ba5-2579f4f6c411"
    )
    assert processor_node.attr["color"] == "yellow"
    assert processor_node.attr["shape"] == "star"
    assert processor_node.attr.get("shape") != default_processor_node.attr.get("shape")
    assert processor_node.attr.get("color") != default_processor_node.attr.get("color")
