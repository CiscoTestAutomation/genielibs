"""Common clear functions for mac"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_mac_address_table_dynamic(device, address=None, interface=None, vlan=None):
    """ Clear mac address-table dynamic
        Args:
            device (`obj`): device object
            address ('str', optional):      mac address, default None
            interface ('str', optional):    interface name, default None
            vlan ('int', optional):         vlan id, default None
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    """

    log.debug('Clearing Dynamic mac address-table on {device}'.format(device=device))

    cmd = "clear mac address-table dynamic"

    # Any combination of these options are in the order of address->interface->vlan
    if address:
        cmd = f"{cmd} address {address}"
    if interface:
        cmd = f"{cmd} interface {interface}"
    if vlan:
        cmd = f"{cmd} vlan {vlan}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure('Could not clear dynamic mac address-table on {device}, Error:\n {error}'.
                                format(device=device, error=e))
