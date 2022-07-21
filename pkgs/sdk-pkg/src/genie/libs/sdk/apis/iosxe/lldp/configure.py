"""Common configure functions for lldp"""

# Python
import logging

#Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_lldp(device):
    """ Enables lldp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    try:
        device.configure('lldp run')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP on interface"
            "Error: {error}".format(error=e)
            )

def unconfigure_lldp(device):
    """ Disables lldp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    try:
        device.configure('no lldp run')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP"
            "Error: {error}".format(error=e)
            )

def configure_lldp_interface(device, interface):
    """ Configure LLDP on interface

        Args:
            device ('obj'): Device object
            interface ('str'): interface on which LLDP to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure LLDP on interface")
    configs = []
    configs.append("lldp run")
    configs.append(f"interface {interface}")
    configs.append("lldp transmit")
    configs.append("lldp receive")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP on interface"
            "Error: {error}".format(error=e)
            )

def unconfigure_lldp_interface(device, interface):
    """ Unconfigure LLDP on interface

        Args:
            device ('obj'): Device object
            interface ('str'): interface on which LLDP to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure LLDP on interface")
    configs = []
    configs.append("no lldp run")
    configs.append(f"interface {interface}")
    configs.append("no lldp transmit")
    configs.append("no lldp receive")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure LLDP on interface"
            "Error: {error}".format(error=e)
            )