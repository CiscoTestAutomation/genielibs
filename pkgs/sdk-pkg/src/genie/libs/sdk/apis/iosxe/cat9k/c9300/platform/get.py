# Python
import logging
import base64
import struct

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)

def get_platform_fan_speed(device):
    """
    Retrieves the fan speeds from the device for Catalyst 9300 series switches.

    Args:
        device (`obj`): Device object.

    Returns:
        A list containing the fan speeds.
        If unable to retrieve fan speeds, returns None.
    """
    fan_speed_info = []

    try:
        # Parse the 'show env fan' command output
        fan_out = device.parse('show env fan')
    except SchemaEmptyParserError as e:
        log.error("Command 'show env fan': {e}".format(e=e))
        return None

    if fan_out and 'switch' in fan_out:
        for switch, switch_data in fan_out['switch'].items():
            for fan, fan_data in switch_data.get('fan', {}).items():
                if 'speed' in fan_data:
                    fan_speed_info.append(fan_data['speed'])

    return fan_speed_info
    
def get_power_supply_info(device):
    """
    Retrieves power supply information for 9300 devices.

    Args:
        device: The device object representing the network device.

    Returns:
        A list containing dictionaries with power supply information.
        If unable to retrieve power supply information, returns an empty list.
    """
    power_supply_info = {}

    try:
        # Retrieve power supply information from the device
        ps_out = device.parse('test platform software database get-n all ios_oper/power_supply_comp')
    except SchemaEmptyParserError as e:
        log.error(f"Failed to retrieve power supply information: {e}")
        return {}

    for ps_entry in ps_out.values():
        for _, ps_data in ps_entry.items():
            ps_name = ps_data.get('ps_name')
            ps_enabled = ps_data.get('ps_enabled')
            ps_capacity = ps_data.get('ps_capacity')

            if ps_enabled == 'true':
                # Extract switch_num and fep_slot from ps_name
                switch_num = ps_name[-3]  
                fep_slot = ps_name[-1]  

                try:
                    # Retrieve detailed power supply statistics
                    fep_out = device.parse(f'test platform hardware fep switch {switch_num} {fep_slot} dump-statistics')
                except SchemaEmptyParserError as e:
                    log.error(f"Failed to retrieve power supply statistics: {e}")
                    return {}

                # Extract required values for the power supply
                input_voltage = fep_out['fru_fep_statistics'].get('input_voltage')
                input_current = fep_out['fru_fep_statistics'].get('input_current')
                input_power = fep_out['fru_fep_statistics'].get('input_power')
                output_voltage = fep_out['fru_fep_statistics'].get('output_voltage')
                output_current = fep_out['fru_fep_statistics'].get('output_current')
                output_power = fep_out['fru_fep_statistics'].get('output_power')

                # Add power supply information to the dictionary
                power_supply_info[ps_name] = {
                    'ps_enabled': ps_enabled,
                    'ps_capacity': base64.b64encode(struct.pack(">f", ps_capacity)).decode("utf-8"),
                    'input_voltage': base64.b64encode(struct.pack(">f", input_voltage)).decode("utf-8"),
                    'input_current': base64.b64encode(struct.pack(">f", input_current)).decode("utf-8"),
                    'input_power': base64.b64encode(struct.pack(">f", input_power)).decode("utf-8"),
                    'output_voltage': base64.b64encode(struct.pack(">f", output_voltage)).decode("utf-8"),
                    'output_current': base64.b64encode(struct.pack(">f", output_current)).decode("utf-8"),
                    'output_power': base64.b64encode(struct.pack(">f", output_power)).decode("utf-8"),
                }

    return power_supply_info
    
