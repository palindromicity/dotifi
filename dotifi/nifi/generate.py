import logging

import jsonpickle
import nipyapi
import pygraphviz as pgv
from nipyapi.nifi import ProcessGroupsEntity


def _add_mock_info(
    do_mock, mock_info_data, function_name, nifi_id=None, args=None, data=None
):
    """
    Populate the mocking information
    :param do_mock: is true mocking data is being track
    :type do_mock: bool
    :param mock_info_data: dict to store mocking information
    :type mock_info_data: dict
    :param function_name: the function call
    :type function_name: str
    :param nifi_id: the nifi uuid involved if applicable
    :type nifi_id: str
    :param args: the function arguments
    :type args: list
    :param data: the return value
    :type data: object
    :return:
    """
    if args is None:
        args = []
    if do_mock:
        if nifi_id is None:
            key = function_name
        else:
            key = "{}:{}".format(function_name, nifi_id)
        mock_info_data[key] = {"args": args, "return": data}


def _create_port_node(subgraph, port_type, port):
    """
    Create a graph node for an input or output port
    :param subgraph: the graph parent of the created node
    :param port_type: a str [input | output]
    :param port: the port object
    :return:
    """
    subgraph.add_node(port.id)
    port_node = subgraph.get_node(port.id)
    port_node.attr["label"] = port.component.name + " : " + port.component.type
    port_node.attr["pos"] = f"{port.position.x:f},{port.position.x:f}"
    port_node.attr["id"] = port.id
    logging.debug(
        "Generate node for %s_port %s:%s", port_type, port.id, port.component.name
    )


def _clone_graph_attrs(source, target):
    """
    Clone one graph's attributes into another graph's
    :param source: the graph from which to take attributes
    :param target: the graph to which to clone the attributes
    :return:
    """
    print(type(source.graph_attr))
    target.graph_attr.update(source.graph_attr)
    target.node_attr.update(source.node_attr)
    target.edge_attr.update(source.edge_attr)


def _handle_group(
    configuration,
    current_depth,
    process_group,
    parent_graph,
    process_group_graph=None,
    do_mock=False,
    mock_info=None,
):
    """
    Generate graph objects for the passed process process_group and add them to the
    parent graph.
    Configuration options will be used to control the depth of the process process_group recursion,
    load templates to overload subgraph settings, and set properties on processors
    If the mock is not empty, then document nipyapi calls.
    :param configuration: confuse.LazyConfig
    :param current_depth: what level of the recursive decent we are on
    :param process_group: the process process_group we are generating graph objects for
    :param parent_graph: the parent of any graph objects we create
    :param process_group_graph: The graph object for this group if it has already been created
    :param do_mock: flag to trun on mock data generation
    :param mock_info: mock data storage
    :return:
    """
    logging.debug("Handling group %s", process_group.id)
    this_flow = nipyapi.canvas.get_flow(process_group.id)
    _add_mock_info(
        do_mock,
        mock_info,
        "nipyapi.canvas.get_flow",
        process_group.id,
        [process_group.id],
        this_flow,
    )

    # Create this group if we have to
    # see if the user has configured a DOT template for this process_group
    if process_group_graph is None:
        if configuration["process_groups"][process_group.id].exists():
            template_file = configuration["process_groups"][process_group.id][
                "template"
            ].as_filename()
            logging.debug(
                "Using template file %s for %d", template_file, process_group.id
            )
            template_group_graph = pgv.AGraph(template_file)
            # process_group_graph = parent_graph.add_subgraph(process_group_graph)
            process_group_graph = parent_graph.add_subgraph(
                name="cluster_" + process_group.component.name
            )
            process_group_graph.graph_attr["id"] = process_group.id
            _clone_graph_attrs(template_group_graph, process_group_graph)
        else:
            process_group_graph = parent_graph.add_subgraph(
                name="cluster_" + process_group.component.name
            )
            process_group_graph.graph_attr["label"] = process_group.component.name
            process_group_graph.graph_attr["id"] = process_group.id
            logging.debug(
                "Created subgraph %s with label %s",
                process_group_graph.name,
                process_group.component.name,
            )

    input_ports = nipyapi.canvas.list_all_input_ports(process_group.id, False)
    _add_mock_info(
        do_mock,
        mock_info,
        "nipyapi.canvas.list_all_input_ports",
        process_group.id,
        [process_group.id, False],
        input_ports,
    )

    for input_port in input_ports:
        _create_port_node(process_group_graph, "input", input_port)

    output_ports = nipyapi.canvas.list_all_output_ports(process_group.id, False)
    _add_mock_info(
        do_mock,
        mock_info,
        "nipyapi.canvas.list_all_output_ports",
        process_group.id,
        [process_group.id, False],
        output_ports,
    )

    for output_port in output_ports:
        _create_port_node(process_group_graph, "output", output_port)

    for processor in this_flow.process_group_flow.flow.processors:
        process_group_graph.add_node(processor.id)
        node = process_group_graph.get_node(processor.id)
        class_full = processor.component.type.split(".")
        node.attr["label"] = (
            processor.component.name + " : " + class_full[len(class_full) - 1]
        )
        node.attr["pos"] = f"{processor.position.x:f},{processor.position.y:f}"
        node.attr["id"] = processor.id
        logging.debug(
            "Generate node for processor %s:%s", processor.id, processor.component.name
        )

        # see if user has configured a set of attributes for this processor
        if configuration["processors"][processor.id]["node_attr"].exists():
            logging.debug("Processor %s has configured attributes", processor.id)
            for key in configuration["processors"][processor.id]["node_attr"]:
                node.attr[key] = configuration["processors"][processor.id]["node_attr"][
                    key
                ].get()
                logging.debug(
                    "Set Processor %s configured attribute %s to %s",
                    processor.id,
                    key,
                    node.attr[key],
                )

    for remote_group in this_flow.process_group_flow.flow.remote_process_groups:
        remote_subgraph = process_group_graph.add_subgraph(
            name="cluster_" + remote_group.component.name
        )
        remote_subgraph.graph_attr["label"] = (
            remote_group.component.target_uri + " : " + "Remote Process Group"
        )
        remote_subgraph.graph_attr["style"] = "filled"
        remote_subgraph.graph_attr["color"] = "blue"
        remote_subgraph.graph_attr["fontcolor"] = "white"
        remote_subgraph.graph_attr["id"] = remote_group.id

        logging.debug(
            "Generate node for Remote Process Group %s:%s",
            remote_group.component.name,
            remote_group.component.target_uri,
        )

        remote_process_group = nipyapi.canvas.get_remote_process_group(
            remote_group.id, summary=True
        )
        _add_mock_info(
            do_mock,
            mock_info,
            "nipyapi.canvas.get_remote_process_group",
            remote_group.id,
            [remote_group.id, True],
            remote_process_group,
        )

        # see if user has configured a set of attributes for this remote process group
        if configuration["remote_process_groups"][remote_group.id][
            "node_attr"
        ].exists():
            logging.debug(
                "Remote Process Group %s has configured attributes",
                remote_group.component.name,
            )
            for key in configuration["remote_process_groups"][remote_group.id][
                "node_attr"
            ]:
                remote_subgraph.graph_attr[key] = configuration[
                    "remote_process_groups"
                ][remote_group.id]["node_attr"][key].get()
                logging.debug(
                    "Set Remote Process Group %s configured graph attribute %s to %s",
                    remote_group.component.name,
                    key,
                    remote_subgraph.graph_attr[key],
                )
        for input_port in remote_process_group["input_ports"]:
            logging.debug(
                "Found Remote Process Group %s input port %s",
                remote_group.component.name,
                input_port.id,
            )
            remote_subgraph.add_node(input_port.id)
            remote_input_port_node = remote_subgraph.get_node(input_port.id)
            remote_input_port_node.attr["label"] = (
                input_port.name + " : " + "INPUT_PORT"
            )
            remote_input_port_node.attr["id"] = input_port.id
            logging.debug(
                "Generated node for Remote Process Group %s input port %s",
                remote_group.component.name,
                input_port.id,
            )
    logging.debug("Checking connections for %s flow", process_group.id)
    for connection in this_flow.process_group_flow.flow.connections:
        if connection.component.selected_relationships is not None:
            for relationship in connection.component.selected_relationships:
                process_group_graph.add_edge(
                    connection.source_id, connection.destination_id
                )
                edge = process_group_graph.get_edge(
                    connection.source_id, connection.destination_id
                )
                edge.attr["label"] = relationship
        else:
            process_group_graph.add_edge(
                connection.source_id, connection.destination_id
            )
            edge = process_group_graph.get_edge(
                connection.source_id, connection.destination_id
            )
            edge.attr["label"] = connection.component.name
        logging.debug(
            "Generated Edge from %s to %s",
            connection.source_id,
            connection.destination_id,
        )

    # check and see if we are at the configured depth or that we can keep going
    configured_depth = int(configuration["depth"].get())
    next_depth = current_depth + 1
    if (configured_depth == -1) or (next_depth <= configured_depth):
        logging.debug("Moving to depth %d", next_depth)
        process_groups_api = nipyapi.nifi.ProcessGroupsApi()
        _add_mock_info(
            do_mock, mock_info, "nipyapi.nifi.ProcessGroupsApi", data=process_groups_api
        )
        inner_process_groups = process_groups_api.get_process_groups(process_group.id)
        if isinstance(inner_process_groups, ProcessGroupsEntity):
            inner_process_groups_actual = inner_process_groups.process_groups
        else:
            inner_process_groups_actual = inner_process_groups

        _add_mock_info(
            do_mock,
            mock_info,
            "ProcessGroupsApi.get_process_groups",
            process_group.id,
            [process_group.id],
            inner_process_groups_actual,
        )
        for inner_process_group in inner_process_groups_actual:
            _handle_group(
                configuration,
                next_depth,
                inner_process_group,
                process_group_graph,
                do_mock=do_mock,
                mock_info=mock_info,
            )
    else:
        logging.debug(
            "Max depth %d met in Process Group %s, stopping",
            configured_depth,
            process_group.id,
        )


def _set_default_root_attrs(root_graph, name="nifi flow"):
    """
    Sets the default attributes for the root graph
    :param root_graph: the graph to configure
    :param name: the graph name
    :return:
    """
    root_graph.node_attr["shape"] = "rectangle"
    root_graph.graph_attr["compound"] = "true"
    root_graph.node_attr["fixedsize"] = "false"
    root_graph.node_attr["fontsize"] = "8"
    root_graph.node_attr["style"] = "filled"
    root_graph.graph_attr["outputorder"] = "edgesfirst"
    root_graph.graph_attr["label"] = name
    root_graph.graph_attr["ratio"] = "1.0"
    root_graph.edge_attr["color"] = "#1100FF"
    root_graph.edge_attr["style"] = "setlinewidth(2)"
    logging.debug("Generated default ROOT_GRAPH")
    logging.debug(root_graph.string())


def generate_graph(generate_configuration) -> pgv.AGraph:
    """
    Walk a NiFi flow and produce an AGraph.
    Configuration options will be used to control the depth of the process group recursion,
    load templates to overload subgraph settings, and set properties on processors
    If the generate-mocks flag is set in options, the mock-file will be written with
    the call data and responses for nipyapi.  This file will be used to create
    mock instances later.
    :param generate_configuration: confuse.LazyConfig
    :return: PyGraphViz AGraph instance
    """
    _root_graph = None
    mock = {}

    logging.debug("generating graph")
    do_mock = generate_configuration["generate_mock_data"].get(bool)
    # check if the user wishes to start somewhere other than the root
    if generate_configuration["start_at_pg"].exists():
        root_id = generate_configuration["start_at_pg"].get()
        logging.debug("using specified start_at_pg %s", root_id)
        root_group = nipyapi.canvas.get_process_group(root_id, identifier_type="id")
        _add_mock_info(
            do_mock,
            mock,
            "nipyapi.canvas.get_process_group",
            args=[root_id, "id"],
            data=root_group,
        )

        # since they are being specific, get the specific template if there is one
        if generate_configuration["process_groups"][root_id].exists():
            template_file = generate_configuration["process_groups"][
                root_id
            ].as_filename()
            logging.debug(
                "specified start_at_pg %s has a configured template %s",
                root_id,
                template_file,
            )
            _root_graph = pgv.AGraph(template_file)
            logging.debug("root graph based on start_at_pg.id and template created")
        else:
            logging.debug(
                "root graph based on start_at_pg will be created from defaults"
            )
            _root_graph = pgv.AGraph(
                name=root_group.component.name + " flow", directed="true", rankdir="LR"
            )
            _set_default_root_attrs(_root_graph, root_group.component.name)

        if "label" not in _root_graph.graph_attr:
            _root_graph.graph_attr["label"] = root_group.component.name
        if "id" not in _root_graph.graph_attr:
            _root_graph.graph_attr["id"] = root_group.id
    else:
        # check if the user has a defined root dot file configured
        # if they do load the root from that
        if generate_configuration["graph"]["template"].exists():
            graph_template_file = generate_configuration["graph"][
                "template"
            ].as_filename()
            logging.debug("Graph has a configured template %s", graph_template_file)
            _root_graph = pgv.AGraph(graph_template_file)
        else:
            logging.debug("root graph will be created from defaults")
            _root_graph = pgv.AGraph(name="nifi flow", directed="true", rankdir="LR")
            _set_default_root_attrs(_root_graph)

        if logging.DEBUG >= logging.root.level:
            logging.debug("ROOT GRAPH : \n%s", _root_graph.string())
        root_id = nipyapi.canvas.get_root_pg_id()
        _add_mock_info(do_mock, mock, "nipyapi.canvas.get_root_pg_id", data=root_id)
        root_group = nipyapi.canvas.get_process_group(root_id, identifier_type="id")
        _add_mock_info(
            do_mock,
            mock,
            "nipyapi.canvas.get_process_group",
            args=[root_id, "id"],
            data=root_group,
        )

    _handle_group(
        generate_configuration, 0, root_group, _root_graph, _root_graph, do_mock, mock
    )

    if do_mock:
        if generate_configuration["mock_data_file"].exists():
            with open(
                generate_configuration["mock_data_file"].as_filename(), "w"
            ) as mock_data_file:
                mock_data_file.write(jsonpickle.encode(mock, make_refs=False))

    return _root_graph
