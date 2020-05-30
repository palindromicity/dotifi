# dotifi

A utility to generate [DOT](https://graphviz.org/doc/info/lang.html) files and images based on [graphviz](https://graphviz.org/documentation/) from the canvas of an [Apache NiFi](https://nifi.apache.org) instance.

### poetry

dotifi is maintained using [poetry](https://python-poetry.org/docs/) for dependency management and packaging.

### Getting started
- Install [Graphviz](https://graphviz.org)
- Clone, fork, or download the [source](https://github.com/palindromicity/dotifi)
- Install [poetry](https://python-poetry.org/docs/)
- If required setup [pyenv](https://github.com/pyenv/pyenv) or your preference to get a python 3.8 environment, as poetry will use whatever the current python is.
    - for example setup pyenv local to the project directory
- In the source route directory run `poetry install`, this will install all the dependencies
- Run `peotry run pytest -v` to run the tests and ensure things are working

#### Setting up [Jetbrains PyCharm](https://www.jetbrains.com/pycharm/) with your virtual python environment
- see [this reddit answer](https://www.reddit.com/r/pycharm/comments/elga2z/using_pycharm_for_poetrybased_projects/fn1ix60?utm_source=share&utm_medium=web2x)

## Configuration
dotify uses [confuse](https://confuse.readthedocs.io/en/latest/) for it's configuration management.
dotify will take it's configuration:

 - from commandline parameters
 - from a yaml configuration file specified with the --with-conf-file parameter
 - some combination of the two

If a configuration file _is_ present, and some configuration value is set both from the commandline and in the configuration,
then the commandline is treated as an override for the configuration file.

String values in the configuration file may be entered as shell environment variables, such as $PATH.  Variables are expanded using
[os.path.expandvars](https://docs.python.org/3/library/os.path.html#os.path.expandvars).

 
```bash
usage: dotify.py [-h] [--with-existing-dot-file EXISTING_GRAPH]
                 [--with-conf-file CONF_NAME]
                 [--output-dot-file OUTPUT_DOT_NAME]
                 [--output-graphviz-fmt {canon,cmap,cmapx,cmapx_np,dia,dot,fig,gd,gd2,gif,hpgl,imap,imap_np,ismap,jpe,jpeg,jpg,mif,mp,pcl,pdf,pic,plain,plain-ext,png,ps,ps2,svg,svgz,vml,vmlz,vrml,vtx,wbmp,xdot,xlib}]
                 [--output-graphviz-file OUTPUT_GRAPHVIZ_BASE_NAME]
                 [--start-at-pg STARTING_PG_ID] [--depth DEPTH]
                 [--nifi-url NIFI_URL] [--using-ssl] [--using-user-pw]
                 [--ca-file CA_FILE] [--client-cert-file CLIENT_CERT_FILE]
                 [--client-key-file CLIENT_KEY_FILE]
                 [--client-key-password CLIENT_KEY_PASSWORD]
                 [--nifi-username NIFI_USER_NAME]
                 [--nifi-user-password NIFI_USER_PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  --with-existing-dot-file EXISTING_GRAPH, -w EXISTING_GRAPH
                        Output will be based on an existing DOT graph
                        definition as opposed to being built from NiFi
  --with-conf-file CONF_NAME, -c CONF_NAME
                        Path to the .yaml file with the configuration. All
                        options can be set in the configuration, with
  --output-dot-file OUTPUT_DOT_NAME, -o OUTPUT_DOT_NAME
                        Path to the dot file to store the dot results to.
  --output-graphviz-fmt {canon,cmap,cmapx,cmapx_np,dia,dot,fig,gd,gd2,gif,hpgl,imap,imap_np,ismap,jpe,jpeg,jpg,mif,mp,pcl,pdf,pic,plain,plain-ext,png,ps,ps2,svg,svgz,vml,vmlz,vrml,vtx,wbmp,xdot,xlib}, -f {canon,cmap,cmapx,cmapx_np,dia,dot,fig,gd,gd2,gif,hpgl,imap,imap_np,ismap,jpe,jpeg,jpg,mif,mp,pcl,pdf,pic,plain,plain-ext,png,ps,ps2,svg,svgz,vml,vmlz,vrml,vtx,wbmp,xdot,xlib}
                        The format of the graphviz generated file. Formats
                        (not all may be available on every system depending on
                        how Graphviz was built)
  --output-graphviz-file OUTPUT_GRAPHVIZ_BASE_NAME, -g OUTPUT_GRAPHVIZ_BASE_NAME
                        Path to the dot file to store the graphviz results to.
                        Results will be saved with the extension of the
                        --output-graphviz-format option
  --start-at-pg STARTING_PG_ID, -s STARTING_PG_ID
                        The id of the process group to start at. This will be
                        a uuid. When set the output will start with this
                        process and it's descendents based on the depth
                        setting
  --depth DEPTH, -d DEPTH
                        The depth to descend to within nested process groups.
                        Note that the top level canvas is the root process
                        group. As such a depth of 0 will only output items in
                        the root canvas and not any process groups it
                        contains. A value of -1 means unlimited.
  --nifi-url NIFI_URL, -n NIFI_URL
                        The url of the NiFi instance to connect to. This is
                        used if --with-existing is not set.
  --using-ssl           Flag, when specified it signals that the NiFi
                        connection requires SSL
  --using-user-pw       Flag, when specified it signals that the NiFi
                        connection requires a username and password
  --ca-file CA_FILE     A PEM file containing certs for the root CA(s) for the
                        NiFi server
  --client-cert-file CLIENT_CERT_FILE
                        A PEM file containing the public certificates for the
                        user / client identity
  --client-key-file CLIENT_KEY_FILE
                        An encrypted (password -protected PEM file containing
                        the client's secret key
  --client-key-password CLIENT_KEY_PASSWORD
                        The password to decrypt the client_key_file
  --nifi-username NIFI_USER_NAME
                        The NiFi user name
  --nifi-user-password NIFI_USER_PASSWORD
                        The NiFi user password

Process finished with exit code 0

```

A sample of the yaml configuration is [here](configurations/sample.yml)

```yaml
# All string values in this configuration may be replaced using
# environmental variables in the form of $VARIABLENAME
#

#  Path to an existing DOT graph definition as opposed to being built from NiFi
with-existing-dot-file:
# Path to the dot file to store the dot results to
output-dot-file:

#  The format of the graphviz generated file. Formats (not all may be available on every system
#  depending on how Graphviz was built
#  "canon", "cmap", "cmapx", "cmapx_np", "dia", "dot", "fig", "gd", "gd2", "gif",
#  "hpgl", "imap", "imap_np", "ismap", "jpe", "jpeg", "jpg", "mif", "mp", "pcl", "pdf",
#  "pic", "plain", "plain-ext", "png", "ps", "ps2", "svg", "svgz", "vml", "vmlz", "vrml",
#  "vtx", "wbmp", "xdot", "xlib"
output-graphviz-fmt:
#  Path to the dot file to store the graphviz results to. Results will be saved with the extension
#  output-graphviz-format option
output-graphviz-file:
#  The id of the process group to start at.  This will be a uuid.  When set the output will start
#  with this process and it's decedents based on the depth setting
start-at-pg:
#  The depth to descend to within nested process groups.  Note that the top level canvas
#  is the root process group.  As such a depth of 0 will only output items in the root canvas and
#  not any process groups it contains.  A value of -1 means unlimited
depth:
# The url of the nifi instance to connect to.  This is used if with-existing is not set
nifi-url:
# Flag, when specified it signals that the NiFi connection requires SSL
using-ssl:
# Flag, when specified it signals that the NiFi connection requires a username and password
using-user-pw:
# A PEM file containing certs for the root CA(s) for the NiFi serve
ca-file:
# A PEM file containing the public certificates for the user / client identity
client-cert-file:
# An encrypted (password -protected PEM file containing the client's secret key
client-key-file:
# The password to decrypt the client_key_file
client-key-password:
# The NiFi user name
nifi-user-name:
# The NiFi user password
nifi-user-password:

# Options for the entire graph
graph:
    # Path to a dot file that contains top level graph definition that sets the properties
    # and attributes at a graph level
    # see https://graphviz.org/documentation/ for information on the dot language
    template: bar.dot
# Options for specific process groups, by id
program_groups:
    # the uuid id of the process group
    351b1dbc-0172-1000-056d-ec78a003b493:
        # Path to a dot file the contains the graph definition that sets the properties
        # and attributes at a graph level for this process group and it's descendents
        template: foo.dot
# Options for specfic processors, by id
processors:
    # the uuid of the processor
    351b1dbc-0172-1000-056d-ec78a003b49:
        # NODE attributes
        # see https://graphviz.gitlab.io/_pages/doc/info/attrs.html
        color: blue

```