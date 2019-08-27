# Steps
from pyats.aetest.steps import Steps

# Unicon
from unicon.core.errors import SubCommandFailure


def configure_syslog_server(device, server):
    """ Configure Syslog servers

        Args:
            device ('obj') : Device to be configured server
            server ('str'): Syslog server to be configured            
            steps ('obj'): Context manager object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure("logging host {ip_address}".format(ip_address=server))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure syslog server "
            "with ip address {ip} on device {dev}".format(
                ip=server, dev=device.name
            )
        )
