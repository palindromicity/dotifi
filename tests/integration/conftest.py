import logging
import pathlib

import docker
import pytest
from docker.errors import ImageNotFound
from nipyapi.utils import DockerContainer

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

host_certs_path = pathlib.Path(__file__).parent.parent.joinpath("resources/docker/keys")


# pylint: disable=R0913
class DotifiDockerContainer(DockerContainer):
    """
    Helper class for Docker container automation without using Ansible
    """

    def __init__(
        self,
        name=None,
        image_name=None,
        image_tag=None,
        ports=None,
        env=None,
        volumes=None,
        test_url=None,
        endpoint=None,
    ):
        super().__init__(
            name, image_name, image_tag, ports, env, volumes, test_url, endpoint
        )
        self.container = None

    def set_container(self, container):
        self.container = container

    def get_container(self):
        return self.container


def _start_docker_containers(docker_containers, network_name="test"):
    """
    Adapted from nipyapi utils

    Deploys a list of DockerContainer's on a given network

    Args:
        docker_containers (list[DockerContainer]): list of Dockers to start
        network_name (str): The name of the Docker Bridge Network to get or
            create for the Docker Containers

    Returns: Nothing

    """
    log.info("Creating Docker client using Environment Variables")
    d_client = docker.from_env()

    # Test if Docker Service is available
    try:
        d_client.version()
    except Exception:
        raise EnvironmentError("Docker Service not found")

    for target in docker_containers:
        assert isinstance(target, DockerContainer)

    # Pull relevant Images
    log.info("Pulling relevant Docker Images if needed")
    for image in set([(c.image_name + ":" + c.image_tag) for c in docker_containers]):
        log.info(f"Checking image {image}")
        try:
            d_client.images.get(image)
            log.info(f"Using local image for {image}")
        except ImageNotFound:
            log.info(f"Pulling {image}")
            d_client.images.pull(image)

    # Clear previous containers
    log.info("Clearing previous containers for this demo")
    d_clear_list = [
        li
        for li in d_client.containers.list(all=True)
        if li.name in [i.name for i in docker_containers]
    ]
    for c in d_clear_list:
        log.info(f"Removing old container {c.name}")
        c.remove(force=True)

    # Deploy/Get Network
    log.info("Getting Docker bridge network")
    d_n_list = [li for li in d_client.networks.list() if network_name in li.name]
    if not d_n_list:
        d_network = d_client.networks.create(
            name=network_name, driver="bridge", check_duplicate=True
        )
    elif len(d_n_list) > 1:
        raise EnvironmentError("Too many test networks found")
    else:
        d_network = d_n_list[0]
    log.info(f"Using Docker network: {d_network.name}")

    # Deploy Containers
    log.info("Starting relevant Docker Containers")
    for c in docker_containers:
        log.info(f"Starting Container {c.name}")
        c.set_container(
            d_client.containers.run(
                image=c.image_name + ":" + c.image_tag,
                detach=True,
                network=network_name,
                hostname=c.name,
                name=c.name,
                ports=c.ports,
                environment=c.env,
                volumes=c.volumes,
                auto_remove=True,
            )
        )


@pytest.fixture
def docker_setup():
    d_network_name = "secure_cluster"

    ldap_env_vars = {
        "AUTH": "ldap",
        "KEYSTORE_PATH": "/opt/certs/localhost-ks.jks",
        "KEYSTORE_TYPE": "JKS",
        "KEYSTORE_PASSWORD": "localhostKeystorePassword",
        "TRUSTSTORE_PATH": "/opt/certs/localhost-ts.jks",
        "TRUSTSTORE_PASSWORD": "localhostTruststorePassword",
        "TRUSTSTORE_TYPE": "JKS",
        "INITIAL_ADMIN_IDENTITY": "nobel",
        "LDAP_AUTHENTICATION_STRATEGY": "SIMPLE",
        "LDAP_MANAGER_DN": "cn=read-only-admin,dc=example,dc=com",
        "LDAP_MANAGER_PASSWORD": "password",
        "LDAP_USER_SEARCH_BASE": "dc=example,dc=com",
        "LDAP_USER_SEARCH_FILTER": "(uid={0})",
        "LDAP_IDENTITY_STRATEGY": "USE_USERNAME",
        "LDAP_URL": "ldap://ldap.forumsys.com:389",
    }

    nifi_container = DotifiDockerContainer(
        name="secure-nifi",
        image_name="apache/nifi",
        image_tag="1.9.1",
        ports={"8443/tcp": 8443},
        env=ldap_env_vars,
        volumes={host_certs_path: {"bind": "/opt/certs", "mode": "ro"}},
    )

    log.info("Starting Secured NiFi Docker Container")
    _start_docker_containers(
        docker_containers=[nifi_container], network_name=d_network_name
    )

    from time import sleep

    sleep(120)

    yield nifi_container
    nifi_container.get_container().kill()


@pytest.fixture
def default_secure_args():
    return {
        "output_dot_file": "nifi_canvas",
        "output_graphviz_format": "png",
        "output_graphviz_program": "dot",
        "output_graphviz_file": "nifi_canvas",
        "depth": -1,
        "nifi_url": "https://localhost:8443/nifi-api",
        "verbose": False,
        "generate_mock_data": False,
        "mock_data_file": "mock_output.json",
        "using_user_pw": True,
        "using_ssl": True,
        "ca_file": host_certs_path.joinpath("localhost-ts.pem").as_posix(),
        "nifi_username": "nobel",
        "nifi_user_password": "password",
        "configure_test_policies": True,
    }
