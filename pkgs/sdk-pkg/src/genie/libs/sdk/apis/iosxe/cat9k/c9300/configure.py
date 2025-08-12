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
    """

        # If the device state is in rommon configure rommon variable
    try:
        connections = getattr(device, 'subconnections', None) or [device]
        for con in connections:
            if con.state_machine.current_state == 'rommon':
                cmd = 'SWITCH_IGNORE_STARTUP_CFG=1'
                con.execute(cmd)
            elif con.role == "standby":
                # If the device is in standby state, skip it since we're already applying the config with "switch all"
                # Otherwise, the standby will fail if locked.
                pass
            else:
                cmd = 'system ignore startupconfig switch all'
                con.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ignore startup config on {device.name}. Error:\n{e}")

def unconfigure_ignore_startup_config(device):
    """ To unconfigure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to unconfigure the device
    """

    try:
        connections = getattr(device, 'subconnections', None) or [device]
        # If the device state is in rommon configure rommon variable
        for con in connections:
            if con.state_machine.current_state == 'rommon':
                cmd = 'SWITCH_IGNORE_STARTUP_CFG=0'
                con.execute(cmd)
            elif con.role == "standby":
                # If the device is in standby state, skip it since we're already applying the config with "switch all"
                # Otherwise, the standby will fail if locked.
                pass
            else:
                cmd = 'no system ignore startupconfig switch all'
                device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ignore startup config on {device.name}. Error:\n{e}")