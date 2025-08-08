# Python
import logging

logger = logging.getLogger(__name__)

from unicon.core.errors import SubCommandFailure

def configure_power_supply_dual(device):
    """Configure power supply dual

    Args:
        device (obj): Device object

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure power supply dual
    """
    try:
        device.configure("power-supply dual")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure power supply dual on {device.name}. Error:\n{e}")
    

def unconfigure_power_supply_dual(device):
    """Unconfigure power supply dual

    Args:
        device (obj): Device object

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure power supply dual
    """
    try:
        device.configure("no power-supply dual")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure power supply dual on {device.name}. Error:\n{e}")
    
