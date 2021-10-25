"""Common configure functions for snmp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

# Genie
from genie.conf.base import Interface


log = logging.getLogger(__name__)

def configure_snmp(device,community_string, access_type):
    """ Configures the snmp on device
        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
            access_type ('str') : type of Access
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring snmp on device {device}".format(device=device))

    try:
        device.configure("snmp-server community {community_string} {access_type}".format(
            community_string=community_string,access_type=access_type))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure snmp. Error:\n{error}".format(error=e))

def unconfigure_snmp(device,community_string):
    """ Unconfigures the snmp on device
        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring snmp on device {device}".format(device=device))

    try:
        device.configure("no snmp-server community {community_string}".format(community_string=community_string))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not unconfigure snmp. Error:\n{error}".format(error=e))
