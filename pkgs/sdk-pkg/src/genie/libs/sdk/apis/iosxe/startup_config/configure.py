# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)


def configure_ignore_startup_config(device):
    """  To configure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure the device
            ValueError : Invalid config register value
    """

    # The bit number 06 of the config register value determines whether to ignore
    # the startup config or not. We must ONLY change this bit and not other bits
    #
    # Reference:
    # https://www.cisco.com/c/en/us/support/docs/routers/10000-series-routers/50421-config-register-use.html

    try:
        # Use the next reload config register value if it is available
        config_reg = device.api.get_config_register(next_reload=True) or \
            device.api.get_config_register()
        config_reg = hex(int(config_reg, 16) | 0x40)
        device.api.execute_set_config_register(config_reg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ignore startup config on {device.name}. Error:\n{e}")
    except ValueError as e:
        raise ValueError(
            f"Could not convert config register value '{config_reg}' to a "
            f"hexadecimal integer. Error:\n{e}"
        )

def unconfigure_ignore_startup_config(device):
    """ To unconfigure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to unconfigure the device
            ValueError : Invalid config register value
    """
    
    try:
        config_reg = device.api.get_config_register(next_reload=True) or \
            device.api.get_config_register()
        config_reg = hex(int(config_reg, 16) & ~0x40)
        device.api.execute_set_config_register(config_reg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ignore startup config on {device.name}. Error:\n{e}")
    except ValueError as e:
        raise ValueError(
            f"Could not convert config register value '{config_reg}' to a "
            f"hexadecimal integer. Error:\n{e}"
        )
