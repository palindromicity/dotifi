"""
Integration test for secure nifi instances with nipi api
adapted from secure_connection.py, nipyapi project.
"""

import logging

import pytest
from dotifi.configuration.load import load_configuration
from dotifi.nifi.connection import configure_nifi_connection
from dotifi.nifi.generate import generate_graph

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.getLogger("nipyapi.utils").setLevel(logging.INFO)
logging.getLogger("nipyapi.security").setLevel(logging.INFO)
logging.getLogger("nipyapi.versioning").setLevel(logging.INFO)


@pytest.mark.skip(reason="disable for github actions")
def test_happy_path(docker_setup, default_secure_args):
    options = load_configuration(default_secure_args, None)
    configure_nifi_connection(options)
    graph = generate_graph(options)
    # base_graph = AGraph(SAMPLE_GRAPH.as_posix())
    assert graph is not None
    # assert graph.number_of_edges() == base_graph.number_of_edges()
    # assert graph.number_of_nodes() == base_graph.number_of_nodes()
    # assert sorted(dict(graph.edges())) == sorted(dict(base_graph.edges()))
    # assert sorted(graph.nodes()) == sorted(base_graph.nodes())
