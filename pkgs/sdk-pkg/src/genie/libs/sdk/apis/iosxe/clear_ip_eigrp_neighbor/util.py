""" Common utility functions for routing"""

# Python
import logging
import ipaddress as ip_addr
import re
from unicon.eal.dialogs import Dialog, Statement
# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)
LOG = log

def clear_ip_eigrp_neighbor(device):
    """
        clear ip eigrp neighbor
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """

    log.debug("clear ip eigrp neighbor")

    try:
        device.execute("clear ip eigrp neighbor")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip eigrp neighbor on {device}. Error:\n{error}".format(device=device, error=e
            )
        ) 