import nipyapi
import pygraphviz as pgv
import logging


def _handle_group(configuration, current_depth, process_group, parent_graph):
    """
    Generate graph objects for the passed process process_group and add them to the
    parent graph.
    Configuration options will be used to control the depth of the process process_group recursion,
    load templates to overload subgraph settings, and set properties on processors
    :param configuration: confuse.LazyConfig
    :param current_depth: what level of the recursive decent we are on
    :param process_group: the process process_group we are generating graph objects for
    :param parent_graph: the parent of any graph objects we create
    :return:
    """
    this_flow = nipyapi.canvas.get_flow(process_group.id)
    # see if the user has configured a DOT template for this process_group
    if configuration['process_groups'][process_group.id].exists():
        template_file = configuration['process_groups']['process_group.id'].as_filename()
        subgraph = pgv.AGraph(template_file)
    else:
        subgraph = parent_graph.add_subgraph(name="cluster_" + process_group.component.name)
        subgraph.graph_attr['label'] = process_group.component.name

    for input_port in nipyapi.canvas.list_all_input_ports(process_group.id, False):
        subgraph.add_node(input_port.id)
        input_node = subgraph.get_node(input_port.id)
        input_node.attr['label'] = input_port.component.name + "\n" + input_port.component.type
        input_node.attr['pos'] = "{0:f},{0:f}".format(input_port.position.x, input_port.position.y)

    for output_port in nipyapi.canvas.list_all_output_ports(process_group.id, False):
        subgraph.add_node(output_port.id)
        output_node = subgraph.get_node(output_port.id)
        output_node.attr['label'] = output_port.component.name + "\n" + output_port.component.type
        output_node.attr['pos'] = "{0:f},{0:f}".format(output_port.position.x, output_port.position.y)

    for processor in this_flow.process_group_flow.flow.processors:
        subgraph.add_node(processor.id)
        node = subgraph.get_node(processor.id)
        class_full = processor.component.type.split(".")
        node.attr['label'] = processor.component.name + "\n" + class_full[len(class_full) - 1]
        node.attr['pos'] = "{0:f},{0:f}".format(processor.position.x, processor.position.y)

        # see if user has configured a set of attributes for this processor
        if configuration['processors'][processor.id].exists():
            for key in configuration['processors'][processor.id]:
                node.attr[key] = configuration['processors'][processor.id][key].get()

    for remote_group in this_flow.process_group_flow.flow.remote_process_groups:
        remote_subgraph = subgraph.add_subgraph(name="cluster_" + remote_group.component.name)
        remote_subgraph.graph_attr['label'] = remote_group.component.target_uri + "\n" + "Remote Process Group"
        remote_subgraph.graph_attr['style'] = 'filled'
        remote_subgraph.graph_attr['color'] = 'blue'
        remote_subgraph.graph_attr['fontcolor'] = 'white'
        remote_process_group = nipyapi.canvas.get_remote_process_group(remote_group.id, summary=True)
        # see if user has configured a set of attributes for this remote process group
        if configuration['remote_process_groups'][remote_group.id].exists():
            for key in configuration['remote_process_groups'][remote_group.id]:
                remote_subgraph.graph_attr[key] = configuration['remote_process_groups'][remote_group.id][key].get()
        for input_port in remote_process_group['input_ports']:
            remote_subgraph.add_node(input_port.id)
            remote_input_port_node = remote_subgraph.get_node(input_port.id)
            remote_input_port_node.attr['label'] = input_port.name + "\n" + "INPUT_PORT"

    for connection in this_flow.process_group_flow.flow.connections:
        if connection.component.selected_relationships is not None:
            for relationship in connection.component.selected_relationships:
                subgraph.add_edge(connection.source_id, connection.destination_id)
                edge = subgraph.get_edge(connection.source_id, connection.destination_id)
                edge.attr['label'] = relationship
        else:
            subgraph.add_edge(connection.source_id, connection.destination_id)
            edge = subgraph.get_edge(connection.source_id, connection.destination_id)
            edge.attr['label'] = connection.component.name

    # check and see if we are at the configured depth or that we can keep going
    configured_depth = int(configuration['depth'].get())
    next_depth = current_depth + 1
    if (configured_depth == -1) or (next_depth <= configured_depth):
        for inner_process_group in nipyapi.nifi.ProcessGroupsApi().get_process_groups(process_group.id).process_groups:
            _handle_group(configuration, next_depth, inner_process_group, subgraph)


def _generate_default_root_attrs(root_graph):
    root_graph.node_attr['shape'] = 'rectangle'
    root_graph.graph_attr['compound'] = 'true'
    root_graph.node_attr['fixedsize'] = 'false'
    root_graph.node_attr['fontsize'] = '8'
    root_graph.node_attr['style'] = 'filled'
    root_graph.graph_attr['outputorder'] = 'edgesfirst'
    root_graph.graph_attr['label'] = "nifi flow"
    root_graph.graph_attr['ratio'] = '1.0'
    root_graph.edge_attr['color'] = '#1100FF'
    root_graph.edge_attr['style'] = 'setlinewidth(2)'


def generate_graph(generate_configuration) -> pgv.AGraph:
    """
    Walk a NiFi flow and produce an AGraph.
    Configuration options will be used to control the depth of the process group recursion,
    load templates to overload subgraph settings, and set properties on processors
    :param generate_configuration: confuse.LazyConfig
    :return: PyGraphViz AGraph instance
    """
    _root_graph = None

    logging.debug("generating graph")
    # check if the user wishes to start somewhere other than the root
    if generate_configuration['starting_pg_id'].exists():
        root_id = generate_configuration['starting_pg_id'].get()
        logging.debug("using specified starting_pg_id %s", root_id)
        # since they are being specific, get the specific template if there is one
        if generate_configuration['process_groups'][root_id].exists():
            template_file = generate_configuration['process_groups'][root_id].as_filename()
            logging.debug("specified starting_pd_id %s has a configured template %s", root_id, template_file)
            _root_graph = pgv.AGraph(template_file)
            logging.debug("root graph based on starting_pg_id and template created")
        else:
            logging.debug("root graph based on starting_pg_id will be created from defaults")
            group = nipyapi.canvas.get_process_group(root_id)
            _root_graph = pgv.AGraph(name=group.component.name + " flow", directed='true', rankdir='LR')
            _generate_default_root_attrs(_root_graph)
            _root_graph.graph_attr['label'] = group.component.name
    else:
        # check if the user has a defined root dot file configured
        # if they do load the root from that
        if generate_configuration['graph']['template'].exists():
            graph_template_file = generate_configuration['graph']['template'].as_filename()
            logging.debug("Graph has a configured template %s", graph_template_file)
            _root_graph = pgv.AGraph(graph_template_file)
        else:
            logging.debug("root graph will be created from defaults")
            _root_graph = pgv.AGraph(name="nifi flow", directed='true', rankdir='LR')
            _generate_default_root_attrs(_root_graph)

        if logging.DEBUG >= logging.root.level:
            logging.debug("ROOT GRAPH : \n%s", _root_graph.string())
        root_id = nipyapi.canvas.get_root_pg_id()

    for process_group in nipyapi.nifi.ProcessGroupsApi().get_process_groups(root_id).process_groups:
        _handle_group(generate_configuration, 1, process_group, _root_graph)

    return _root_graph
