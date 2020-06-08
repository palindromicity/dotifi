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
GRAPH_TEMPLATE_CONFIG = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "resources/graph_template.yaml"
)
PG_TEMPLATE_CONFIG = pathlib.Path(__file__).parent.parent.parent.joinpath(
    "resources/pg_template.yaml"
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
    Test overriding the graph_attr of a specific remote process group
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
    assert rpg_subgraph.graph_attr.get("color") == "yellow"
    assert rpg_subgraph.graph_attr.get("shape") == "star"
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
    :param path to the configuration
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
    assert processor_node.attr.get("color") == "yellow"
    assert processor_node.attr.get("shape") == "star"
    assert processor_node.attr.get("shape") != default_processor_node.attr.get("shape")
    assert processor_node.attr.get("color") != default_processor_node.attr.get("color")


@pytest.mark.parametrize("path_arg", [HAPPY_MOCK_DATA])
def test_graph_template(default_args):
    """
    Test overriding the root graph configuration
    using the yaml configuration specified dot file
    :param default_args the default_args fixture
    :param path to the configuration
    """

    options = load_configuration(default_args, GRAPH_TEMPLATE_CONFIG.as_posix())
    options["graph"]["template"] = (
        pathlib.Path(__file__)
        .parent.parent.parent.joinpath(
            "resources/" + options["graph"]["template"].get()
        )
        .as_posix()
    )
    graph = generate_graph(options)
    base_graph = AGraph(SAMPLE_GRAPH.as_posix())
    assert graph is not None
    assert graph.number_of_edges() == base_graph.number_of_edges()
    assert graph.number_of_nodes() == base_graph.number_of_nodes()
    assert sorted(dict(graph.edges())) == sorted(dict(base_graph.edges()))
    assert sorted(graph.nodes()) == sorted(base_graph.nodes())
    assert graph.graph_attr.get("label") == "My Business"
    assert graph.node_attr.get("shape") == "circle"
    assert graph.node_attr.get("shape") != base_graph.node_attr.get("shape")
    assert graph.graph_attr.get("label") != base_graph.graph_attr.get("label")


@pytest.mark.parametrize("path_arg", [HAPPY_MOCK_DATA])
def test_pg_template(default_args):
    """
    Test overriding the graph configuration of a specific process group
    using the yaml configuration specified dot file
    :param default_args the default_args fixture
    :param path to the configuration
    """

    options = load_configuration(default_args, PG_TEMPLATE_CONFIG.as_posix())
    options["process_groups"]["351dbb56-0172-1000-21fa-a4af9fc0dbb1"]["template"] = (
        pathlib.Path(__file__)
        .parent.parent.parent.joinpath(
            "resources/"
            + options["process_groups"]["351dbb56-0172-1000-21fa-a4af9fc0dbb1"][
                "template"
            ].get()
        )
        .as_posix()
    )
    graph = generate_graph(options)
    base_graph = AGraph(SAMPLE_GRAPH.as_posix())
    assert graph is not None
    assert graph.number_of_edges() == base_graph.number_of_edges()
    assert graph.number_of_nodes() == base_graph.number_of_nodes()
    assert sorted(dict(graph.edges())) == sorted(dict(base_graph.edges()))
    assert sorted(graph.nodes()) == sorted(base_graph.nodes())
    pg_subgraph = _find_subgraph(graph, "351dbb56-0172-1000-21fa-a4af9fc0dbb1")
    default_subgraph = _find_subgraph(
        base_graph, "351dbb56-0172-1000-21fa-a4af9fc0dbb1"
    )
    assert pg_subgraph.graph_attr.get("label") == "My Business"
    assert pg_subgraph.node_attr.get("shape") == "circle"
    assert pg_subgraph.edge_attr.get("style") == "dashed"

    assert pg_subgraph.graph_attr.get("label") != default_subgraph.graph_attr.get(
        "label"
    )
    assert pg_subgraph.node_attr.get("shape") != default_subgraph.node_attr.get("shape")
    assert pg_subgraph.edge_attr.get("style") != default_subgraph.edge_attr.get("style")
