'''IOSXE execute functions for hw-module'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)


def hw_module_switch_usbflash_security_password(device, switch_number, action, pwd):
   
    """  Execute hw-module switch <switch_number> usbflash1 security enable or diasble password
            Args:
            device ('obj'): device to use
            switch_number ('str'): switch number
            action ('str') : enable or disable
            pwd ('str') : password

        Returns:
            output
        Raises:
            SubCommandFailure exception
    """
    cmd = f"hw-module switch {switch_number} usbflash1 security {action} password {pwd}"
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not {action} hw-module on device {device}. Error:\n{e}")
    return output