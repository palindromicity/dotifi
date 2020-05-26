import argparse
from dotifi.util.configuration import load_configuration


def process():
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-existing-dot-file", "-w", dest="existing_graph", required=False,
                        help="Output will be based on an existing DOT graph definition as opposed to being built " +
                             "from NiFi")
    parser.add_argument("--with-conf-file", "-c", dest="conf_name", required=False,
                        help="Path to the .yaml file with the configuration. All options can be set in the " +
                             "configuration, with ")
    parser.add_argument("--output-dot-file", "-o", dest="output_dot_name", default="./nifi-canvas.dot", required=False,
                        help="Path to the dot file to store the dot results to.")
    parser.add_argument("--output-graphviz-fmt", "-f", dest="output_graphviz_format", required=False, default="png",
                        help="The format of the graphviz generated file. Formats " +
                             "(not all may be available on every system depending on how Graphviz was built)",
                        choices=["canon", "cmap", "cmapx", "cmapx_np", "dia", "dot", "fig", "gd", "gd2", "gif",
                                 "hpgl", "imap", "imap_np", "ismap", "jpe", "jpeg", "jpg", "mif", "mp", "pcl",
                                 "pdf",
                                 "pic", "plain", "plain-ext", "png", "ps", "ps2", "svg", "svgz", "vml", "vmlz",
                                 "vrml",
                                 "vtx", "wbmp", "xdot", "xlib"])
    parser.add_argument("--output-graphviz-file", "-g", dest="output_graphviz_base_name", default="nifi-canvas",
                        required=False,
                        help="Path to the dot file to store the graphviz results to. " +
                             "Results will be saved with the extension " +
                             "of the --output-graphviz-format option")
    parser.add_argument("--start-at-pg", "-s", dest="starting_pg_id", required=False,
                        help="The id of the process group to start at.  This will be a uuid.  " +
                             "When set the output will start " +
                             "with this process and it's descendents based on the depth setting")
    parser.add_argument("--depth", "-d", dest="depth", default="-1", required=False,
                        help="The depth to descend to within nested process groups.  Note that the top level canvas " +
                             "is the root process group.  As such a depth of 0 will only output items in the root " +
                             "canvas and not any process groups it contains. A value of -1 means unlimited.")
    parser.add_argument("--nifi-url", "-n", dest="nifi_url", default="http://localhost:8080/nifi", required=False,
                        help="The url of the NiFi instance to connect to.  This is used if --with-existing is not set."
                        )
    parser.add_argument("--using-ssl", dest="use_ssl", action="store_true", required=False, default=False,
                        help="Flag, when specified it signals that the NiFi connection requires SSL"
                        )
    parser.add_argument("--using-user-pw", dest="use_user_pass", action="store_true", required=False, default=False,
                        help="Flag, when specified it signals that the NiFi connection requires a username and password"
                        )
    parser.add_argument("--ca-file", dest="ca_file", required=False,
                        help="A PEM file containing certs for the root CA(s) for the NiFi server"
                        )
    parser.add_argument("--client-cert-file", dest="client_cert_file", required=False,
                        help="A PEM file containing the public certificates for the user / client identity"
                        )
    parser.add_argument("--client-key-file", dest="client_key_file", required=False,
                        help="An encrypted (password -protected PEM file containing the client's secret key"
                        )
    parser.add_argument("--client-key-password", dest="client_key_password", required=False,
                        help="The password to decrypt the client_key_file"
                        )
    parser.add_argument("--nifi-username", dest="nifi_user_name", required=False,
                        help="The NiFi user name"
                        )
    parser.add_argument("--nifi-user-password", dest="nifi_user_password", required=False,
                        help="The NiFi user password")
    args = vars(parser.parse_args())

    options = load_configuration(args, args['conf_name'])
    print("foo")


if __name__ == "__main__":
    process()
