"""Common configure functions for NTP"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def remove_ntp_system_peer(device, system_peer):
    """ Remove ntp system peer config

        Args:
            device (`obj`): Device object
            system_peer ('str'): System peer IP address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no ntp server {}".format(system_peer))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in removing ntp system "
            "peer {system_peer} on device {device}, "
            "Error: {e}".format(system_peer=system_peer, device=device.name, e=str(e))
        ) from e


def remove_ntp_server(device, servers):
    """ Remove all configured server using routes

        Args:
            device ('obj'): Device object
            servers ('list'): List of servers to remove(server)
                ex.)
                    servers = ['192.168.36.11', '192.168.36.12']
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = []
    for route in servers:
        config.append("no ntp server {}".format(route))

    try:
        device.configure("\n".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in removing ntp servers "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_ntp_master(device, stratum=None):
    """ Configure ntp master

        Args:
            device ('obj'): Device object
            stratum ('str'): Specify a different stratum level 
                from which NTP clients get their time synchronized. 
                The range is from 1 to 15.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if not stratum or stratum >= 1 and stratum <= 15:
        try:
            device.configure("ntp master {}".format("" if not stratum else stratum))
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Failed in configuring ntp master "
                "on device {device}, "
                "Error: {e}".format(device=device.name, e=str(e))
            ) from e
    else:
        raise SubCommandFailure(
            "Invalid input. Stratum value must "
            "be empty or integer value between 1 and 15"
        )


def configure_ntp_iburst(device, route):
    """ Configure ntp iburst using ip address

        Args:
            device ('obj'): Device object
            route ('str'): IP address to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("ntp server {} iburst".format(route))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring ntp iburst "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e


def configure_ntp_server(device, ntp_config, auth_key=None, unconfig=False):
    """ Configures ntp server

        Args:
            device ('obj'): device to configure on
            ntp_config ('list'): List containing server ip address
                ex.)
                   ntp_config = [ 
                        '192.168.1.1',
                        '192.168.1.2'
                    ]
            auth_key ('list'): Authentication key number corresponding
                               to server ip
                ex.)
                   auth_key = [
                        '1',
                        '2',
                   ]
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if not isinstance(ntp_config, list) and not isinstance(auth_key, list):
        raise SubCommandFailure("ntp_config or auth_key must be a list")

    config = []
    if auth_key:
        if len(ntp_config) != len(auth_key):
            raise SubCommandFailure("ntp_config and auth_key should have same number of value in list")
    for num, ip in enumerate(ntp_config):
        if unconfig:
            cmd = "no ntp server {ip}".format(ip=ip)
        else:
            cmd = "ntp server {ip}".format(ip=ip)

        if auth_key:
            cmd += " key {auth_key}".format(auth_key=auth_key[num])

        config.append(cmd)

    try:
        device.configure("\n".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring ntp server "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e
