import logging


def publish(publish_configuration, graph):
    """
    Publishes a graph to a dot file and to a graphical file
    :param publish_configuration: confuse.LazyConfig
    :param graph: PyGraphViz.AGraph
    :return:
    """

    dot_name = publish_configuration['output_dot_name'].as_filename()
    logging.debug("Graph will be written as dot file: %s", dot_name)

    graphic_base_name = publish_configuration['output_graphviz_name'].as_filename()
    graphviz_fmt = publish_configuration['output_graphviz_format'].as_choice(
        ["canon", "cmap", "cmapx", "cmapx_np", "dia", "dot", "fig", "gd", "gd2", "gif",
         "hpgl", "imap", "imap_np", "ismap", "jpe", "jpeg", "jpg", "mif", "mp", "pcl",
         "pdf",
         "pic", "plain", "plain-ext", "png", "ps", "ps2", "svg", "svgz", "vml", "vmlz",
         "vrml",
         "vtx", "wbmp", "xdot", "xlib"])

    graph.write(dot_name)
    graph.draw(graphic_base_name, prog=graphviz_fmt)
