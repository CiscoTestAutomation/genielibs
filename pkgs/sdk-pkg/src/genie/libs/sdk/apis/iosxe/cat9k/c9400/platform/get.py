# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)

def get_platform_fan_speed(device):
    """
    Retrieves the fan speeds from the device for Catalyst 9400 series switches.

    Args:
        device: The device object representing the network device.

    Returns:
        A list containing the fan speeds.
        If unable to retrieve fan speeds, returns None.
    """
    fan_speed_info = []

    try:
        # Parse the 'show platform hardware chassis fantray detail' command output
        fan_out = device.parse('show platform hardware chassis fantray detail')
    except SchemaEmptyParserError as e:
        log.error("Command 'show platform hardware chassis fantray detail': {e}".format(e=e))
        return None

    if fan_out and 'fantray_details' in fan_out:
        for row, row_data in fan_out.get('fantray_details', {}).items():
            for fan_name, speed in row_data.get('fan', {}).items():
                if speed != 'N/A':
                    fan_speed_info.append(int(speed))

    return fan_speed_info