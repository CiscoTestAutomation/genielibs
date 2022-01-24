# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


def get_boot_variables(device, boot_var, output=None):
    '''Get current or next-reload boot variables on the device
        Args:
            device (`obj`): Device object
            boot_var (`str`): Type of boot variable to return to caller
            output (`str`): output from show boot
        Returns:
            List of boot images or []
        Raises:
            Exception
    '''

    # Check type
    assert boot_var in ['current', 'next']

    boot_images = []
    try:
        parsed = device.parse("show boot", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show boot' did not return any output\n{}".\
                  format(str(e)))
    else:
        # Get current or next
        if boot_var == 'current':
            boot_variables = parsed.get("active", {}).get("boot_variable")
            if boot_variables is None:
                    boot_variables = parsed.get("current_boot_variable")
        else:
            boot_variables = parsed.get("active", {}).get("boot_variable")
            if boot_variables is None:
                    boot_variables = parsed.get("next_reload_boot_variable")

        # Trim
        if boot_variables:
            for item in boot_variables.split(';'):
                if not item:
                    continue
                if ',' in item:
                    item, num = item.split(',')
                if " " in item:
                    item, discard = item.split(" ")
                boot_images.append(item)

    return boot_images


def get_config_register(device, next_reload=False, output=None):
    '''Get current config-register setting on the device
        Args:
            device (`obj`): Device object
            next_reload (`bool`): Determine if returning next-reload value
        Returns:
            config-register value or None
    '''

    try:
        parsed = device.parse("show version", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any output\n{}".\
                  format(str(e)))
        return None

    # Check if next_reload is set
    if next_reload :
        return parsed.get('version', {}).get('next_config_register')
    else:
        return parsed.get('version', {}).get('curr_config_register')