"""Common configure functions for arp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_arp_timeout(device, interface, timeout):
    """ Config arp timeout on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            timeout (`int`): timeout in second
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring arp timeout on interface {} with value {}".format(
            interface, timeout
        )
    )
    try:
        device.configure(
            [
                "interface {}".format(interface),
                "arp timeout {}".format(timeout),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring arp timeout "
            "on interface {interface} with value {timeout} "
            "on device {device}, "
            "Error: {e}".format(
                interface=interface,
                timeout=timeout,
                device=device.name,
                e=str(e),
            )
        ) from e


def remove_arp_timeout(device, interface):
    """ Remove arp timeout configuration

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Removing arp timeout on interface {}".format(interface))
    try:
        device.configure(["interface {}".format(interface), "no arp timeout"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in removing arp timeout "
            "on interface {interface} "
            "on device {device}, "
            "Error: {e}".format(
                interface=interface, device=device.name, e=str(e)
            )
        ) from e


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
    log.info("Configuring static arp")
    try:
        device.configure(
            "arp {ip_address} {mac_address} arpa".format(
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
