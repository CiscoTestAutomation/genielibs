'''IOSXE Common configure functions for Metaluna LC'''

# Unicon
from unicon.core.errors import SubCommandFailure

def configure_400g_mode_for_port_group(device, slot, port_group):
    """ enable 400g mode conversion on Metaluna LC
        Args:
            device (`obj`): Device object
            slot (`int`): Metaluna slot
            port_group ('int'): port group number

        Returns:
            None

        Raises:
            SubCommandFailure : Failed configuring device
    """

    try:
        device.configure('hw-module slot {slot} port-group {port_group} mode 400G'.format(slot=slot,port_group=port_group))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mode conversion on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_400g_mode_for_port_group(device, slot, port_group):
    """ disable 400g mode conversion on Metaluna LC
        Args:
            device (`obj`): Device object
            slot (`int`): Metaluna slot
            port_group ('int'): port group number

        Returns:
            None

        Raises:
            SubCommandFailure : Failed configuring device
    """

    try:
        device.configure('no hw-module slot {slot} port-group {port_group} mode 400G'.format(slot=slot,port_group=port_group))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mode conversion on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_400g_mode_port_group_range(device, slot):
    """ enable 400g mode range conversion on Metaluna LC
        Args:
            device (`obj`): Device object
            slot (`int`): Metaluna slot

        Returns:
            None

        Raises:
            SubCommandFailure : Failed configuring device
    """

    try:
        device.configure('hw-module slot {slot} port-group range 1-2 mode 400G'.format(slot=slot))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mode conversion on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_400g_mode_port_group_range(device, slot):
    """ disable 400g mode range conversion on Metaluna LC
        Args:
            device (`obj`): Device object
            slot (`int`): Metaluna slot

        Returns:
            None

        Raises:
            SubCommandFailure : Failed configuring device
    """

    try:
        device.configure('no hw-module slot {slot} port-group range 1-2 mode 400G'.format(slot=slot))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mode conversion on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
