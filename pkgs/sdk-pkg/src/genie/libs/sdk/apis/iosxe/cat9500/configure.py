# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def configure_tacacs_server(device, server_config):
    """ Configure tacacs server
        Args:
            device ('obj'): Device object
            server_config('dict'): Dictionary object
                dictionary contains following  keys:
                    host ('str'): host ip address
                    timeout ('int'): server time out value in seconds
                    key_type (str): key type for tacacs server
                    key ('str'): key value from tacacs server
                    server ('str'): server ip address
                    ipv6_server('str'): server ipv6 address
                    single_connection('boolean'): set to True
                    send_nat_address('boolean'): set to True
                    fqdn_name('str'): Fully Qualified domain name
            Returns:
                configurations list
            Raises:
                Failed configuring tacacs server
            Example:
                server_config = {
                            'host': 'mgmt-tac',
                            'timeout': '10',
                            'key_type': '7',
                            'key': '01239132C123',
                            'server': '192.168.21.1'
                            'ipv6_server': '2000::2'
                            'single_connection': True
                            'send_nat_address': True
                            'fqdn_name': 'f1'
                        },
    """

    config = []

    # tacacs server mgmt-tac
    if "host" in server_config:
        config.append("tacacs server {0}".format(server_config["host"]))

    # address ipv4 10.106.26.213
    if "server" in server_config:
        config.append("address ipv4 {0}".format(server_config["server"]))

    # address ipv6 200::4
    if "ipv6_server" in server_config:
        config.append("address ipv6 {0}".format(server_config["ipv6_server"]))

    # key 0 Cisco123
    if "key_type" in server_config and "key" in server_config:
        config.append("key {0} {1}".format(server_config["key_type"],
                                             server_config["key"]))
    # key Cisco123
    elif "key" in server_config:
        config.append("key {0}".format(server_config["key"]))

    # timeout 10
    if "timeout" in server_config:
        config.append("timeout {0}".format(server_config["timeout"]))

    # single-connection
    if server_config.get("single_connection", False):
        config.append("single-connection")

    # send-nat-address
    if server_config.get("send_nat_address", False):
        config.append("send-nat-address")

    # address fqdn f1
    if 'fqdn_name' in server_config:
        config.append("address fqdn {0}".format(server_config["fqdn_name"]))

    try:
        device.configure(config)
        return config
    except SubCommandFailure as e:
        logger.error(f"Failed to configure tacacs server with error {e}")
        raise
