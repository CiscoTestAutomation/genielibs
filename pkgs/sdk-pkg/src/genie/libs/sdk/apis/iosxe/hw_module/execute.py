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


def hw_module_sub_slot_reload(device, sub_slot):
    """ hw-module sub-slot {slot} reload force
        Args:
            device (`obj`): Device object
            sub_slot (`str`): sub_slot

        Returns:
            Shutdown Status

        Raises:
            SubCommandFailure : Failed configuring device
    """
    cmd = 'hw-module subslot {slot} reload force\n'.format(slot=sub_slot)
    try:
        return device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not reload hw-module slot {slot}. Error:\n{error}"
                .format(slot=sub_slot, error=e)
        )

def hw_module_filesystem_security_lock(device, filesystem, operation):
    """ Enable/Disable Security-lock on filesystem bootflash/harddisk
        Args:
            device ('obj'): Device object
            filesystem('str'): Filesystem (bootflash/harddisk)
            operation('str'): Enable/Disable

    """

    cmd = f"hw-module {filesystem} security-lock {operation}"
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to {operation} security-lock on filesystem:{filesystem}. Error:\n{e}")
    return output
