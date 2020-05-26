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
    '''

    # Check type
    assert boot_var in ['current', 'next']

    boot_images = []
    try:
        boot_out = device.parse("show boot", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show boot' did not return any output\n{}".\
                  format(str(e)))
    else:
        # Get current or next
        if boot_var == 'current':
            if boot_out.get("active", {}):
                boot_variables = boot_out.get("active", {}).get("boot_variable")
            else:
                boot_variables = boot_out.get("current_boot_variable")
        else:
            if boot_out.get("active", {}):
                boot_variables = boot_out.get("active", {}).get("boot_variable")
            else:
                boot_variables = boot_out.get("next_reload_boot_variable")

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

