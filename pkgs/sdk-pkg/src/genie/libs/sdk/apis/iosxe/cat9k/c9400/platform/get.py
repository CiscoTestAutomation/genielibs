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

def get_power_supply_info(device):
    """
    Retrieves power supply information for 9400 devices.

    Args:
        device: The device object representing the network device.

    Returns:
        A dictionary containing power supply information.
        If unable to retrieve power supply information, returns an empty dictionary.
    """
    power_supply_info = {}

    try:
        env_out = device.parse('show env status')
    except SchemaEmptyParserError as e:
        log.error("Command 'show env status': {e}".format(e=e))
        return {}

    power_supply_data = env_out.get('power_supply', {})
    for ps_name, ps_details in power_supply_data.items():
        if ps_details.get('status') == 'active':
            capacity = ps_details.get('capacity')
            enabled = 'True' if ps_details.get('status') == 'active' else 'false'

            try:
                power_supply_detail_out = device.parse('show platform hardware chassis power-supply detail all')
            except SchemaEmptyParserError as e:
                log.error("Command 'show platform hardware chassis power-supply detail all': {e}".format(e=e))
                return {}

            power_supply_details = power_supply_detail_out.get('power_supplies', {}).get(ps_name, {})
            if power_supply_details:
                # Extract input and output values
                input_values = {key: value for key, value in power_supply_details.get('input', {}).items() if value != 'n.a'}
                output_values = {key: value for key, value in power_supply_details.get('output', {}).items() if value != 'n.a'}

                # Map keys from input and output values
                input_mapping = {'current_a': 'input_current', 'power_a': 'input_power', 'voltage_a': 'input_voltage'}
                output_mapping = {'current': 'output_current', 'power': 'output_power', 'voltage': 'output_voltage'}

                # Generate keys using the mappings
                input_info = {input_mapping.get(key, key): value for key, value in input_values.items()}
                output_info = {output_mapping.get(key, key): value for key, value in output_values.items()}

                # Get the module name based on the PS name
                numeric_part = ''.join(filter(str.isdigit, ps_name))
                module_name = f'PowerSupplyModule{numeric_part}'

                # Encode values and add to power supply info dictionary
                power_supply_info[module_name] = {
                     'ps_enabled': enabled,  # Assuming all active power supplies are enabled
                    'ps_capacity': base64.b64encode(struct.pack(">f", float(capacity))).decode("utf-8"),
                    **{key: base64.b64encode(struct.pack(">f", float(value))).decode("utf-8") for key, value in input_info.items()},
                    **{key: base64.b64encode(struct.pack(">f", float(value))).decode("utf-8") for key, value in output_info.items()}
                }

    return power_supply_info
