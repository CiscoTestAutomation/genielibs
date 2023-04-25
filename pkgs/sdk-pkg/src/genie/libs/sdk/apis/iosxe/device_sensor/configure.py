"""Common configure functions for device sensor"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_device_sensor_filter_list(device, protocol, list_name, tlv_name=None, tlv_number=None, option_name=None, option_number=None):
    """ Configure device sensor filter list
    
    Args:
        device ('obj'): device to use
        protocol ('str'): Protocol names like cdp, dhcp, lldp.
        list_name ('str'): Protocol list name.
        tlv_name ('str', optional): TLV type list name. Default is None.
        tlv_number ('int', optional): TLV type list number. Default is None.
        option_name ('str', optional): Option type list name. Default is None.
        option_number ('str', optional): Option type list name. Default is None.
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure device sensor filter list
    """

    cmd = [f'device-sensor filter-list {protocol} list {list_name}']
    if tlv_name:
        cmd.append(f'tlv name {tlv_name}')
    if tlv_number:
        cmd.append(f'tlv number {tlv_number}')
    if option_name:
        cmd.append(f'option name {option_name}')
    if option_number:
        cmd.append(f'option number {option_number}')
    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure device sensor filter list. Error:\n{e}")


def unconfigure_device_sensor_filter_list(device, protocol, list_name, tlv_name=None, tlv_number=None, option_name=None, option_number=None, filter_list=False):
    """ Unconfigure device sensor filter list
    
    Args:
        device ('obj'): device to use
        protocol ('str'): Protocol names like cdp, dhcp, lldp.
        list_name ('str'): Protocol list name.
        tlv_name ('str', optional): TLV type list name. Default is None.
        tlv_number ('int', optional): TLV type list number. Default is None.
        option_name ('str', optional): Option type list name. Default is None.
        option_number ('str', optional): Option type list name. Default is None.
        filter_list ('bool', optional): Unconfigures filter-list name. Default is False.
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure device sensor filter list
    """

    cmd = [f'device-sensor filter-list {protocol} list {list_name}']
    if tlv_name:
        cmd.append(f'no tlv name {tlv_name}')
    if tlv_number:
        cmd.append(f'no tlv number {tlv_number}')
    if option_name:
        cmd.append(f'no option name {option_name}')
    if option_number:
        cmd.append(f'no option number {option_number}')
    if filter_list:
        cmd = [f'no device-sensor filter-list {protocol} list {list_name}']
    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure device sensor filter list. Error:\n{e}")
