''' Common Config functions for IOXE / Spanning-tree '''

import logging
import time

log = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout

def configure_spanning_tree_portfast(device, default=False, bpduguard=False, bpdufilter=False, mode='edge'):
    """ Configures Spanning Tree Portfast
        Args:
            device ('obj')    : device to use
            default ('boolean', optional) : Configure spanning-tree portfast default. Default is False
            bpdugaurd ('boolean', optional) : Configure spanning-tree portfast bpduguard. Default is False
            bpdufilter ('boolean', optional) : Configure spanning-tree bpdufilter default. Default is False
            mode ('str', optional) : Portfast mode. Default is edge
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"spanning-tree portfast {mode} "
    if bpduguard:
        config += "bpduguard default" if default else "bpduguard"
    elif bpdufilter:
        config += "bpdufilter default"
    elif default:
        config += "default"

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure spanning-tree portfast - Error:\n{error}'
        )


def unconfigure_spanning_tree_portfast(device, default=False, bpduguard=False, bpdufilter=False, mode='edge'):
    """ Unconfigures Spanning Tree Portfast
        Args:
            device ('obj')    : device to use
            default ('boolean', optional) : Unconfigure spanning-tree portfast default. Default is False
            bpdugaurd ('boolean', optional) : Unconfigure spanning-tree portfast bpduguard. Default is False
            bpdufilter ('boolean', optional) : Unconfigure spanning-tree bpdufilter default. Default is False
            mode ('str', optional) : Portfast mode. Default is edge
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"no spanning-tree portfast {mode} "
    if bpduguard:
        config += "bpduguard default" if default else "bpduguard"
    elif bpdufilter:
        config += "bpdufilter default"
    elif default:
        config += "default"

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure spanning-tree portfast - Error:\n{error}'
        )
