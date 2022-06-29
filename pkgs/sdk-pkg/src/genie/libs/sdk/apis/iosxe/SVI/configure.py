"""Common configure functions for SVI"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_SVI_Unnumbered(device, interface, loopback):
    """ Configure SVI interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface vlan (Ex: Vlan500)
            loopback ('str'): Unnumbered loopback (Ex: Loopback1)    
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure SVI interface
    """
    log.info(
        "Configuring SVI interface={} ".format(interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "ip unnumbered {}".format(loopback),
                "ipv6 unnumbered {}".format(loopback),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure SVI interface {interface}".format(
                interface=interface
            )
        )

def configure_SVI_Autostate(device, interface):
    """ Configure SVI Interface state
        Args:
            device ('obj'): device to use
            interface ('str'): interface vlan (Ex: vlan500)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure SVI interface state
    """
    log.info("Configuring SVI interface state")
    try:
        device.configure(
            [
                "interface {}".format(interface),
                "no autostate",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not SVI state {interface}".format(
                interface=interface
            )
        )

