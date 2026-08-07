"""Common execute functions for sisf"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def enable_device_tracking_debug(device, destination_guard=False, vlan_id=None, errors=False):
    """ Enable device-tracking debug.

        Args:
            device ('obj'): Device object
            destination_guard ('bool', optional): Enable destination-guard debug.
                Defaults to False.
            vlan_id ('str', optional): VLAN id for destination-guard debug.
                Required when destination_guard is True.
            errors ('bool', optional): Enable device-tracking errors debug.
                Defaults to False.

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to enable device-tracking debug
            ValueError: destination_guard debug was requested without vlan_id
    """
    if destination_guard and not vlan_id:
        raise ValueError('vlan_id is required when destination_guard is True')

    if destination_guard:
        cmd = f'debug device-tracking destination-guard vlanid {vlan_id}'
    elif errors:
        cmd = 'debug device-tracking errors'
    else:
        cmd = 'debug device-tracking'

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not enable device-tracking debug on {device}. Error:\n{e}'
        )


def disable_device_tracking_debug(device, destination_guard=False, vlan_id=None, errors=False):
    """ Disable device-tracking debug.

        Args:
            device ('obj'): Device object
            destination_guard ('bool', optional): Disable destination-guard debug.
                Defaults to False.
            vlan_id ('str', optional): VLAN id for destination-guard debug.
                Required when destination_guard is True.
            errors ('bool', optional): Disable device-tracking errors debug.
                Defaults to False.

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to disable device-tracking debug
            ValueError: destination_guard debug was requested without vlan_id
    """
    if destination_guard and not vlan_id:
        raise ValueError('vlan_id is required when destination_guard is True')

    if destination_guard:
        cmd = f'undebug device-tracking destination-guard vlanid {vlan_id}'
    elif errors:
        cmd = 'undebug device-tracking errors'
    else:
        cmd = 'no debug device-tracking'

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not disable device-tracking debug on {device}. Error:\n{e}'
        )