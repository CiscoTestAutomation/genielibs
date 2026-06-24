"""Common configure functions for arp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_static_arp(device, ip_address, mac_address):
    """ Configure static arp

        Args:
            device (`obj`): Device object
            ip_address (`str`): IP address
            mac_address (`str`): MAC address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring static arp")
    try:
        device.configure(
            "arp {ip_address} {mac_address} ARPA".format(
                ip_address=ip_address, mac_address=mac_address
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring static arp "
            "with IP address {ip_address} "
            "and MAC address {mac_address} "
            "on device {device}, "
            "Error: {e}".format(
                ip_address=ip_address,
                mac_address=mac_address,
                device=device.name,
                e=str(e),
            )
        ) from e


def unconfigure_static_arp(device, ip_address, mac_address):
    """ unconfigure static arp

        Args:
            device (`obj`): Device object
            ip_address (`str`): IP address
            mac_address (`str`): MAC address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("unconfiguring static arp")
    try:
        device.configure(
            "no arp {ip_address} {mac_address} ARPA".format(
                ip_address=ip_address, mac_address=mac_address
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in unconfiguring static arp "
            "with IP address {ip_address} "
            "and MAC address {mac_address} "
            "on device {device}, "
            "Error: {e}".format(
                ip_address=ip_address,
                mac_address=mac_address,
                device=device.name,
                e=str(e),
            )
        ) from e
