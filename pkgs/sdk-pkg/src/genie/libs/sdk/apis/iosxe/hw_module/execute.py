'''IOSXE execute functions for hw-module'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

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


def hw_module_sub_slot_stop(device, sub_slot):
    """ Execute 'hw-module subslot <sub_slot> stop' on the device
        Args:
            device ('obj'): Device object
            sub_slot (`str`): sub_slot
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.info("Executing 'hw-module subslot <sub_slot> stop' on the device")

    # Unicon Statement/Dialog
    dialog = Dialog([
             Statement(
                pattern=r".*Proceed with stop of module? [confirm]",
                action='sendline()',
                loop_continue=True,
                continue_timer=False)
             ])
    command = f'hw-module subslot {sub_slot} stop'

    try:
        device.execute(
                 command,
                 reply=dialog,
                 append_error_pattern=['.*Command cannot be executed.*'])
    except SubCommandFailure as err:
        raise SubCommandFailure(
            "Could not stop hw-module subslot {sub_slot}. Error:\n{error}"
            .format(sub_slot=sub_slot, error=e)
        )


def hw_module_sub_slot_start(device, sub_slot):
    """ Execute 'hw-module subslot <sub_slot> start' on the device
        Args:
            device ('obj'): Device object
            sub_slot (`str`): sub_slot
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.info("Executing 'hw-module subslot <sub_slot> start' on the device")

    command = f'hw-module subslot {sub_slot} start'

    try:
        device.execute(
                 command,
                 append_error_pattern=['.*Command cannot be executed.*'])
    except SubCommandFailure as err:
        raise SubCommandFailure(
            "Could not start hw-module subslot {sub_slot}. Error:\n{error}"
            .format(sub_slot=sub_slot, error=e)
        )
        

def hw_module_sub_slot_oir_power_cycle(device, sub_slot):
    """ Execute 'hw-module subslot <sub_slot> oir power-cycle' on the device
        Args:
            device ('obj'): Device object
            sub_slot (`str`): sub_slot
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.info("Executing 'hw-module subslot <sub_slot> oir power-cycle' on the device")

    # Unicon Statement/Dialog
    dialog = Dialog([
             Statement(
                pattern=r".*Proceed with power cycle of module? [confirm]",
                action='sendline()',
                loop_continue=True,
                continue_timer=False)
             ])
    command = f'hw-module subslot {sub_slot} oir power-cycle'

    try:
        device.execute(
                 command,
                 reply=dialog,
                 append_error_pattern=['.*Command cannot be executed.*'])
    except SubCommandFailure as err:
        raise SubCommandFailure(
            "Could not oir power-cycle hw-module subslot {sub_slot}. Error:\n{error}"
            .format(sub_slot=sub_slot, error=e)
        )
