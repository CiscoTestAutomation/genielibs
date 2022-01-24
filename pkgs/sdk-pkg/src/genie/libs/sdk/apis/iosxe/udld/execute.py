"""Common execute functions for udld"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


log = logging.getLogger(__name__)

def execute_udld_tx_drop(device, interface):
    """ Configures UDLD transmission drop on Interface 
    Args:
        device (`obj`): Device object
        interface (`str`): interface
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring interface
    """
    try:
        device.execute(f'test udld int {interface} tx-drop')
    except SubCommandFailure as e:
        raise SubCommandFailure(
        'Could not configure udld transmission drop on {interface}, Error: {error}'.format(
            interface=interface, error=e))