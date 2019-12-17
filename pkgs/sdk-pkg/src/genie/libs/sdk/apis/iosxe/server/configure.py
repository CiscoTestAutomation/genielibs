"""Common configure functions for TACACS server"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_tacacs_server(device, server_config):

    """ Configure tacacs server

        Args:
            device ('obj'): Device object
            server_config('list'): List of configuration for server
                dictionary contains following 3 keys:
                    host ('str'): host ip address
                    timeout ('int'): server time out value in seconds
                    key_type ('int'): key type for tacacs server
                    key ('str'): key value from tacacs server
                    server ('str'): server ip address
                ex.)
                    [
                        {
                            'host': '192.168.21.1',
                            'timeout': 10,
                            'key_type': 7,
                            'key': '01239132C123',
                            'server': '192.168.21.1'
                        },
                        {
                            'host': '192.168.21.2',
                            'timeout': 10,
                            'key_type': 7,
                            'key': '01239132C123',
                            'server': '192.168.21.2'
                        }
                    ] 
                        
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring tacacs server 
    """

    config = []
    for sc in server_config:
        if "host" in sc:
            config.append("tacacs server {}\n".format(sc["host"]))
            config.append("address ipv4 {}\n".format(sc["host"]))
        if "timeout" in sc:
            config.append("timeout {}\n".format(sc["timeout"]))
        if "key_type" in sc and "key" in sc:
            config.append(
                "key {} {}\n".format(sc["key_type"], sc["key"])
            )

        config.append("exit\n")

        try:
            device.configure("".join(config))
        except SubCommandFailure:
            raise SubCommandFailure(
                "Could not configure tacacs server on device {device}".format(
                    device=device.name
                )
            )
