"""Common configure functions for offline provisioning"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_switch_provision(device, switch_number, sku_type):
    """ Configures switch provisioning / offline configuration
        Example : switch 3 provision c9300-24h

        Args:
            device ('obj'): device to use
            switch_number('int'): switch number (Range 1-16)
            sku_type('str'): type of switch

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f"Configuring switch provision {sku_type} on switch {switch_number} on {device.name}")
    config = f"switch {switch_number} provision {sku_type}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switch provision {sku_type} on device {device.name}. Error:\n{e}")

def unconfigure_switch_provision(device, switch_number, sku_type=None):
    """ Unconfigures switch provisioning
        Example : no switch 3 provision / no switch 3 provision C9300-24U

        Args:
            device ('obj'): device to use
            switch_number('int'): switch number (Range 1-16)
            sku_type('str'): type of switch

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f"Unconfiguring switch provision on switch {switch_number} on {device.name}")
    if sku_type:
        config = f"no switch {switch_number} provision {sku_type}"
    else:
        config = f"no switch {switch_number} provision"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure switch {switch_number} provision on device {device.name}. Error:\n{e}")
