import logging


def publish(publish_configuration, graph):
    """
    Publishes a graph to a dot file and to a graphical file
    :param publish_configuration: confuse.LazyConfig
    :param graph: PyGraphViz.AGraph
    :return:
    """

    dot_name = publish_configuration['output_dot_file'].as_filename()
    logging.debug("Graph will be written as dot file: %s", dot_name)

    graphic_base_name = publish_configuration['output_graphviz_file'].as_filename()
    graphic_program = publish_configuration['output_graphviz_program'].get()
    graphviz_fmt = publish_configuration['output_graphviz_format'].as_choice(
        ["canon", "cmap", "cmapx", "cmapx_np", "dia", "dot", "fig", "gd", "gd2", "gif",
         "hpgl", "imap", "imap_np", "ismap", "jpe", "jpeg", "jpg", "mif", "mp", "pcl",
         "pdf",
         "pic", "plain", "plain-ext", "png", "ps", "ps2", "svg", "svgz", "vml", "vmlz",
         "vrml",
         "vtx", "wbmp", "xdot", "xlib"])

    if not graphic_base_name.endswith(graphviz_fmt):
        graphic_base_name = graphic_base_name + "." + graphviz_fmt
    if not dot_name.endswith(".dot"):
        dot_name = dot_name + ".dot"
    graph.write(dot_name)
    graph.draw(graphic_base_name, prog=graphic_program, format=graphviz_fmt)
