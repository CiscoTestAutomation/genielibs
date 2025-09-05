# Python
import os
import re
import logging
import time

# pyATS
from pyats.easypy import runtime
from pyats.utils.objects import R, find

# Genie
from genie.utils import Dq
from genie.utils.diff import Diff
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import (SchemaEmptyParserError,
                                              SchemaMissingKeyError)
from genie.libs.parser.iosxe.show_logging import ShowLogging
from datetime import datetime, timedelta, timezone

# Unicon
from unicon.core.errors import SubCommandFailure

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
                log.info(f"Boot images set using boot_variable on active device: {boot_variables}")
            else:
                for each in ["current_boot_variable", "boot_variable"]:
                    if boot_out.get(each):
                        boot_variables = boot_out.get(each)
                        log.info(f"Boot images set using {each} -> {boot_variables}")
                        break

        else:
            if boot_out.get("active", {}):
                boot_variables = boot_out.get("active", {}).get("boot_variable")
                log.info(f"Boot images set using boot_variable on active device: {boot_variables}")
            else:
                for each in ["next_reload_boot_variable", "boot_variable"]:
                    if boot_out.get(each):
                        boot_variables = boot_out.get(each)
                        log.info(f"Boot images set using {each} -> {boot_variables}")
                        break

            if boot_variables is None:
                boot_variables = boot_out.get("next_reload_boot_variable")
                log.info(f"Boot images set using next_reload_boot_variable -> {boot_variables}")

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
    """Get current config-register setting on the device
        Args:
            device (`obj`): Device object
            next_reload (`bool`): Determine if returning next-reload value
        Returns:
            config-register value or None
    """

    try:
        version_out = device.parse("show version", output=output)
    except Exception as e:
        log.error(f"Command 'show version' did not return any output or failed to parse: {e}")
        return None

    current_cr_key = 'curr_config_register'
    next_reload_cr_key = 'next_config_register'
    parsed_data = version_out.get('version', version_out)

    if next_reload:
        if next_reload_cr_key in parsed_data:
            return parsed_data.get(next_reload_cr_key)
        else:
            log.warning(f"'{next_reload_cr_key}' not found in 'show version' parsed output. "
                        f"Attempting to return current config register if available.")
            if current_cr_key in parsed_data:
                return parsed_data.get(current_cr_key)
            else:
                log.warning(f"Neither '{next_reload_cr_key}' nor '{current_cr_key}' found in 'show version' output. Returning None.")
                return None
    else:
        if current_cr_key in parsed_data:
            return parsed_data.get(current_cr_key)
        else:
            log.warning(f"'{current_cr_key}' not found in 'show version' parsed output. Returning None.")
            return None