# Python
import logging
"""Common configure functions for interface"""
'''IOSXE Common configure functions for Metaluna LC'''

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)
       
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

def configure_hw_module_breakout(device,
        breakout_number,
        breakout_number_end_range=None,
        switch_number = None,
        ):
    """ 
        Configures hw_module breakout
        Args:
             device ('obj'): device to use
             breakout_number ('str'): breakout number
             breakout_number_end_range ('str') : range end for breakout
             switch_number('int') : switch number 1 or 2

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring hw-module breakout {breakout_number} ".format(
            breakout_number=breakout_number
        )
    )

    if switch_number is not None:
        if breakout_number_end_range is not None:
            cmd = [f"hw-module switch {switch_number} breakout range {breakout_number} {breakout_number_end_range}"]
        else:
            cmd = [f"hw-module switch {switch_number} breakout {breakout_number}"]    
    else:
        if breakout_number_end_range is not None:
             cmd = [f"hw-module breakout range {breakout_number} {breakout_number_end_range}"]
        else:     
            cmd = [f"hw-module breakout {breakout_number}"]
    
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure hw_module breakout. Error:\n{error}".format(
                error=e
            )
        )

def unconfigure_hw_module_breakout(device,
        breakout_number,
        breakout_number_end_range=None,
        switch_number = None,
        ):
    """
        Unconfigures hw_module breakout
        Args:
             device ('obj'): device to use
             breakout_number ('str'): breakout number 
             breakout_number_end_range ('str') : range end for breakout
             switch_number('int') : switch number 1 or 2

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring hw-module breakout {breakout_number} ".format(
            breakout_number=breakout_number
        )
    )

    if switch_number is not None:
        if breakout_number_end_range is not None:
            cmd = [f"no hw-module switch {switch_number} breakout range {breakout_number} {breakout_number_end_range}"]
        else:
            cmd = [f"no hw-module switch {switch_number} breakout {breakout_number}"]
    else:
        if breakout_number_end_range is not None:
            cmd = [f"no hw-module breakout range {breakout_number} {breakout_number_end_range}"]
        else:    
            cmd = [f"no hw-module breakout {breakout_number}"]

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure hw_module breakout. Error:\n{error}".format(
                error=e
            )
        )
