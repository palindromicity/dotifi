import logging


def publish(publish_configuration, graph):
    """
    Publishes a graph to a dot file and to a graphical file
    :param publish_configuration: confuse.LazyConfig
    :param graph: PyGraphViz.AGraph
    :return:
    """

    dot_name = publish_configuration["output_dot_file"].as_filename()
    logging.debug("Graph will be written as dot file: %s", dot_name)
    graphic_file_name = publish_configuration["output_graphviz_file"].as_filename()
    graphic_program = publish_configuration["output_graphviz_program"].get()
    graphviz_fmt = publish_configuration["output_graphviz_format"].as_choice(
        [
            "canon",
            "cmap",
            "cmapx",
            "cmapx_np",
            "dia",
            "dot",
            "fig",
            "gd",
            "gd2",
            "gif",
            "hpgl",
            "imap",
            "imap_np",
            "ismap",
            "jpe",
            "jpeg",
            "jpg",
            "mif",
            "mp",
            "pcl",
            "pdf",
            "pic",
            "plain",
            "plain-ext",
            "png",
            "ps",
            "ps2",
            "svg",
            "svgz",
            "vml",
            "vmlz",
            "vrml",
            "vtx",
            "wbmp",
            "xdot",
            "xlib",
        ]
    )

    if not graphic_file_name.endswith(graphviz_fmt):
        graphic_file_name = graphic_file_name + "." + graphviz_fmt
    if not dot_name.endswith(".gv"):
        dot_name = dot_name + ".gv"

    graph.write(dot_name)
    logging.debug("Wrote %s", dot_name)
    graph.draw(graphic_file_name, prog=graphic_program, format=graphviz_fmt)
    logging.debug(
        "Wrote %s prog= %s  format=%s", graphic_file_name, graphic_program, graphviz_fmt
    )
