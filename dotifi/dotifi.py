import argparse
import logging

from confuse import NotFoundError
from pygraphviz import AGraph

from dotifi.configuration.load import load_configuration
from dotifi.nifi import generate
from dotifi.nifi.connection import configure_nifi_connection
from dotifi.publishing.publish import publish

"""
dotifi main script
dotifi will, based on configuration, produce a .dot file and image file from a Apache Nifi canvas.
"""


def process():
    """
    dotifi process function, handles parameter checking, merging with possible configuration files and executing
    the generation
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-existing-dot-file",
        "-w",
        required=False,
        help="Output will be based on an existing DOT graph definition as opposed to being built "
        + "from NiFi",
    )
    parser.add_argument(
        "--with-conf-file",
        "-c",
        required=False,
        help="Path to the .yaml file with the configuration. All options can be set in the "
        + "configuration, with ",
    )
    parser.add_argument(
        "--output-dot-file",
        "-o",
        required=False,
        default="nifi-canvas",
        help="Path to the gv file to store the dot results to.",
    )
    parser.add_argument(
        "--output-graphviz-format",
        "-f",
        default="png",
        help="The format of the graphviz generated file. Formats "
        + "(not all may be available on every system depending on how Graphviz was built)",
        choices=[
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
        ],
    )
    parser.add_argument(
        "--output-graphviz-program",
        required=False,
        default="dot",
        help="Graphviz layout method to use.",
        choices=["neato", "dot", "twopi", "circo", "fdp", "nop"],
    )
    parser.add_argument(
        "--output-graphviz-file",
        "-g",
        required=False,
        default="nifi-canvas",
        help="Path to the graphical file to store the graphviz results to. "
        + "Results will be saved with the extension "
        + "of the --output-graphviz-format option",
    )
    parser.add_argument(
        "--start-at-pg",
        "-s",
        required=False,
        help="The id of the process group to start at.  This will be a uuid.  "
        + "When set the output will start "
        + "with this process and it's descendents based on the depth setting",
    )
    parser.add_argument(
        "--depth",
        "-d",
        required=False,
        default="-1",
        help="The depth to descend to within nested process groups.  Note that the top level canvas "
        + "is the root process group.  As such a depth of 0 will only output items in the root "
        + "canvas and not any process groups it contains. A value of -1 means unlimited.",
    )
    parser.add_argument(
        "--nifi-url",
        "-n",
        required=False,
        default="http://localhost:8080/nifi-api",
        help="The url of the NiFi instance to connect to.  This is used if --with-existing is not set.",
    )
    parser.add_argument(
        "--using-ssl",
        action="store_true",
        required=False,
        default=False,
        help="Flag, when specified it signals that the NiFi connection requires SSL",
    )
    parser.add_argument(
        "--using-user-pw",
        action="store_true",
        required=False,
        default=False,
        help="Flag, when specified it signals that the NiFi connection requires a username and password",
    )
    parser.add_argument(
        "--ca-file",
        required=False,
        help="A PEM file containing certs for the root CA(s) for the NiFi server",
    )
    parser.add_argument(
        "--client-cert-file",
        required=False,
        help="A PEM file containing the public certificates for the user / client identity",
    )
    parser.add_argument(
        "--client-key-file",
        required=False,
        help="An encrypted (password -protected PEM file containing the client's secret key",
    )
    parser.add_argument(
        "--client-key-password",
        required=False,
        help="The password to decrypt the client_key_file",
    )
    parser.add_argument("--nifi-username", required=False, help="The NiFi user name")
    parser.add_argument(
        "--nifi-user-password", required=False, help="The NiFi user password"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        required=False,
        default=False,
        help="Sets the logging level to verbose",
    )
    parser.add_argument(
        "--generate-mock-data",
        action="store_true",
        required=False,
        default=False,
        help="Generates mock data",
    )
    parser.add_argument(
        "--mock-data-file",
        required=False,
        default="mock_output.json",
        help="When --generate-mock-data is specified, it will be written to this file",
    )
    args = vars(parser.parse_args())

    options = load_configuration(args, args.get("with_conf_file"))

    level = logging.WARNING
    if options["verbose"].get():
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s",
        force=True,
    )
    # logging.root.setLevel(level)

    logging.debug("Configuration:\n%s", options.dump())

    graph = None
    if options["with_existing_dot_file"].exists():
        existing_path = options["with_existing_dot_file"].as_filename()
        logging.debug("Using existing DOT file %s", existing_path)
        try:
            graph = AGraph(existing_path)
            logging.debug("Loaded graph from %s :\n%s", existing_path, graph.string())
        except FileNotFoundError as e:
            logging.exception(e)
            exit(1)
    else:
        try:
            configure_nifi_connection(options)
            graph = generate.generate_graph(options)
        except (NotFoundError, Exception, ValueError) as e:
            logging.exception(e)
            exit(1)

    publish(options, graph)


if __name__ == "__main__":
    process()
