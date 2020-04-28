# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)

def get_boot_variables(device, output=None):
    '''Get current boot variables on the device
        Args:
            device (`obj`): Device object
            output (str): output from show boot
        Returns:
            List of boot images or []
    '''

    boot_images = []
    try:
        boot_out = device.parse("show boot", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show boot' did not return any output\n{}".\
                  format(str(e)))
    else:
        boot_variables = boot_out.get("next_reload_boot_variable")
        if boot_variables:
            for item in boot_variables.split(';'):
                if ',' in item:
                    image, num = item.split(',')
                    boot_images.append(image)
                else:
                    boot_images.append(item)

    return boot_images