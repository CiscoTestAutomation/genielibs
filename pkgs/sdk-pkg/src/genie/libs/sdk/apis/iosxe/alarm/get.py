'''IOSXE get functions for alarms '''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)


def get_alarm_max_min_temp(device):
    """ Get the maximum and minimum temperature from the device from alarm settings

        Args:
            device (`obj`): Device object

        Returns:
            list: list with max and min temperature

        Raises:
            SubCommandFailure: Failed to get the max and min temperature
    """
    
    try:
        output = device.parse('show alarm settings')
        max_temp = output['temperature_primary']['threshold']['max_temp']
        min_temp = output['temperature_primary']['threshold']['min_temp']
    except KeyError:
        raise SubCommandFailure(
            f"Could not find max or min temperature in output of 'show alarm settings' on device {device.name}."
        )

    return [max_temp, min_temp]


def get_alarm_contact_relay_mode(device):
    """ Get the contact relay mode from the device from alarm settings

        Args:
            device (`obj`): Device object

        Returns:
            str: contact relay mode

        Raises:
            SubCommandFailure: Failed to get the contact relay mode
    """
    
    try:
        output = device.parse('show alarm settings')
        contact_relay_mode = output.get('alarm_relay_mode', 'N/A')

        if contact_relay_mode == 'N/A':
            raise KeyError
        
    except KeyError:
        raise SubCommandFailure(
            f"Could not find contact relay mode in output of 'show alarm settings' on device {device.name}."
        )

    return contact_relay_mode