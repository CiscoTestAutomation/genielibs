"Unshut hw-module slot {slot}"
"Shut hw-module slot {slot}"


import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)
       
def unconfigure_hw_module_slot_shutdown(device, slot):
    """ Unshut hw-module slot {slot}
        Args:
            device (`obj`): Device object
            slot (`int`): slot

        Returns:
            Shutdown Status

        Raises:
            SubCommandFailure : Failed configuring device
    """

    cmd = 'no hw-module slot {slot} shutdown'.format(slot=slot)
    try:
        result = device.configure(cmd)
        return result
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unshut hw-module slot {slot}. Error:\n{error}"
                .format(slot=slot, error=e)
        )

def configure_hw_module_slot_shutdown(device, slot):
    """ Shut hw-module slot {slot}
        Args:
            device (`obj`): Device object
            slot (`int`): slot

        Returns:
            Shutdown Status

        Raises:
            SubCommandFailure : Failed configuring device
    """
    cmd = 'hw-module slot {slot} shutdown'.format(slot=slot)
    try:
        result = device.configure(cmd)
        return result

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not shutdown hw-module slot {slot}. Error:\n{error}"
                .format(slot=slot, error=e)
        )


def unconfigure_hw_module_sub_slot_shutdown(device, sub_slot):
    """ Configure 'no hw-module subslot <sub_slot> shutdown unpowered' on the device
        Args:
            device ('obj'): Device object
            sub_slot (`str`): sub_slot
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = 'no hw-module subslot {sub_slot} shutdown unpowered'.format(sub_slot=sub_slot)
    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unshut hw-module subslot {sub_slot}. Error:\n{error}"
            .format(sub_slot=sub_slot, error=e)
        )


def configure_hw_module_sub_slot_shutdown(device, sub_slot):
    """ Configure 'hw-module subslot <sub_slot> shutdown unpowered' on the device
        Args:
            device ('obj'): Device object
            sub_slot (`str`): sub_slot
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = 'hw-module subslot {sub_slot} shutdown unpowered'.format(sub_slot=sub_slot)
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not shutdown hw-module subslot {sub_slot}. Error:\n{error}"
            .format(sub_slot=sub_slot, error=e)
        )
