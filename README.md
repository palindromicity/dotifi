# dotifi

A utility to generate [DOT](https://graphviz.org/doc/info/lang.html) files and images based on [graphviz](https://graphviz.org/documentation/) from the canvas of an [Apache NiFi](https://nifi.apache.org) instance.

```bash
/Users/ottofowler/Library/Caches/pypoetry/virtualenvs/dotifi-bdSYdp08-py3.8/bin/python /Users/ottofowler/src/github/ottobackwards/forks/dotifi/dotifi/dotify.py --help
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