import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_hw_module_switch_slot_shutdown(device, switch_num, slot=None, subslot=None):
    """ Shut hw-module slot {slot}
        Args:
            device (`obj`): Device object
            slot (`int`): slot
            subslot (`int`): subslot
            switch_num (`int`): switch number 

        Returns:
            Shutdown Status

        Raises:
            SubCommandFailure : Failed configuring device
    """
    if slot:
        cmd = f"hw-module switch {switch_num} slot {slot} shutdown"
        identifier = f"slot {slot}"
    else:
        cmd = f"hw-module switch {switch_num} subslot {subslot} shutdown"
        identifier = f"subslot {subslot}"
    try:
        result = device.configure(cmd)
        return result

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not shutdown hw-module switch {switch_num} {identifier}. Error:\n{e}"
        )

def unconfigure_hw_module_switch_slot_shutdown(device, switch_num, slot=None, subslot=None):
    """ Shut hw-module slot {slot}
        Args:
            device (`obj`): Device object
            slot (`int`): slot
            subslot (`int`): subslot
            switch_num (`int`): switch number 

        Returns:
            Shutdown Status

        Raises:
            SubCommandFailure : Failed configuring device
    """
    if slot:
        cmd = f"no hw-module switch {switch_num} slot {slot} shutdown"
        identifier = f"slot {slot}"
    else:
        cmd = f"no hw-module switch {switch_num} subslot {subslot} shutdown"
        identifier = f"subslot {subslot}"
    try:
        result = device.configure(cmd)
        return result

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unshutdown hw-module switch {switch_num} {identifier}. Error:\n{e}"
        )