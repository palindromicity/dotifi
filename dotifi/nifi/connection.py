import nipyapi
import logging


def configure_nifi_connection(configuration):
    """
    Configure the NiFi connection based on the configuration
    :param configuration: confuse.LazyConfig
    """
    if logging.DEBUG >= logging.root.level:
        logging.debug("setting nifi endpoint to %s", configuration['nifi_url'].get())
    nipyapi.utils.set_endpoint(configuration['nifi_url'].get())

    if configuration['using_ssl'].exists() and configuration['using_ssl'].get(bool):
        if 'https://' not in configuration['nifi_url'].get():
            raise Exception("Configured for ssl without an https nifi-url")
        ca_file = None
        if configuration['ca_file'].exists():
            ca_file = configuration['ca_file'].as_filename()
            logging.debug("setting ca_file to %s", ca_file)
        client_cert_file = None
        if configuration['client_cert_file'].exists():
            client_cert_file = configuration['client_cert_file'].as_filename()
            logging.debug("setting client_cert_file to %s", client_cert_file)
        client_key_file = None
        if configuration['client_key_file'].exists():
            client_key_file = configuration['client_key_file'].as_filename()
            logging.debug("setting client_key_file to %s", client_key_file)
        client_key_password = None
        if configuration['client_key_password'].exists():
            client_key_password = configuration['client_key_password'].get()
            logging.debug("setting client_key_password")
        nipyapi.security.set_service_ssl_context(ca_file, client_cert_file, client_key_file, client_key_password)
        logging.debug("SSL context setup")
        username = None
        password = None
        if configuration['using_user_pass'].exists() and configuration['using_user_pass'].get(bool):
            logging.debug("Configured for user / password authentication")
            username = configuration['nifi_user_name'].get()
            logging.debug("nifi_user_name is %s", username)
            password = configuration['nifi_user_password'].get()
            logging.debug("attempting to log into nifi")
            nipyapi.utils.wait_to_complete(
                test_function=nipyapi.security.service_login,
                service='nifi',
                username=username,
                password=password,
                bool_response=True,
                nipyapi_delay=nipyapi.config.long_retry_delay,
                nipyapi_max_wait=nipyapi.config.long_max_wait
            )
            nifi_user = nipyapi.security.get_service_access_status(service='nifi')
            logging.debug(
                'nipyapi_secured_nifi CurrentUser: ' + nifi_user.access_status.identity
            )







