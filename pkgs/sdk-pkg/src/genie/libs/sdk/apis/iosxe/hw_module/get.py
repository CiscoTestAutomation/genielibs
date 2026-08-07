"""Common get info functions for hw_module"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_hw_module_subslot_oir(device, subslot):
    """Get OIR status of a specific subslot in a hardware module

    Args:
        device ('obj'): Device object
        subslot ('str'): Subslot identifier
    Returns:
        Dict with OIR status of the subslot
    """
    try:
        return device.parse(f'show hw-module subslot {subslot} oir')
    except SchemaEmptyParserError as e:
        log.debug(f'Could not get OIR status for subslot {subslot}, '
                  f'Error: {e}')
        return None


def get_platform_hardware_subslot_module_interface_status(
        device, subslot, interface):
    """Get interface status of a specific subslot in a hardware module

    Args:
        device ('obj'): Device object
        subslot ('str'): Subslot identifier
        interface ('str'): Interface identifier
    Returns:
        Dict with interface status of the subslot
    """
    try:
        return device.parse(
            f'show platform hardware subslot {subslot} module '
            f'interface {interface} status')
    except SchemaEmptyParserError as e:
        log.debug(
            f'Could not get interface status for subslot {subslot}, '
            f'interface {interface}, Error: {e}')
        return None
