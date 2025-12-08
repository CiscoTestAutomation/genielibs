"""Common configure functions for DNS"""


# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ip_host(
    device, 
    hostname,
    ip_address,
    **kwargs,
):
    """ Configure ip host with domain name and ip address 
        Args:
            device ('obj'): device to use
            hostname ('str'): Name of the host
            ip_address ('str'): IP Address of the host
        Returns:
            console output
        Raises:
            SubCommandFailure: ip host configuration
    """

    cmd = f"domain ipv4 host {hostname} {ip_address}"
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip host. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_ip_host(
    device, 
    hostname,
    ip_address,
    **kwargs,
):
    """ Enable ip name server 
        Args:
            device ('obj'): device to use
            hostname ('str'): Name of the host
            ip_address ('str'): IP Address of the host
        Returns:
            console output
        Raises:
            SubCommandFailure: ip host Un-configuration
    """

    cmd = f"no domain ipv4 host {hostname} {ip_address}"
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Un-configure ip host. Error:\n{error}".format(error=e)
        )
    return out