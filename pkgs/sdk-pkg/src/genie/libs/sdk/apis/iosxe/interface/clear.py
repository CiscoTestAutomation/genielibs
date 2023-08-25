# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


# Logger

log = logging.getLogger(__name__)

def clear_interface_range(device, interface, interface_range):
    """ clear interface range
        Args:
            device (`obj`): Device object
            interface('str'): interface name
            interface_range('str'): interface range
        Return:
            None
        Raise:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'default interface range {interface} {interface_range}')
    cmd.append(f'no interface range {interface} {interface_range}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not clear interface range on {interface}. Error:\n{e}"
        )