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

    try:
        connections = getattr(device, 'subconnections', None) or [device]
        for con in connections:
            # If the device state is in rommon configure rommon variable
            if con.state_machine.current_state == 'rommon':
                cmd = 'SWITCH_IGNORE_STARTUP_CFG=1'
                con.execute(cmd)
            elif con.role == "standby":
                # If the device is in standby state, skip it since we're already applying the config with "switch all"
                # Otherwise, the standby will fail if locked.
                pass
            else:
                cmd = 'system ignore startupconfig'
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
        for con in connections:
            # If the device state is in rommon configure rommon variable
            if con.state_machine.current_state == 'rommon':
                cmd = 'SWITCH_IGNORE_STARTUP_CFG=0'
                con.execute(cmd)
            elif con.role == "standby":
                # If the device is in standby state, skip it since we're already applying the config with "switch all"
                # Otherwise, the standby will fail if locked.
                pass
            else:
                cmd = 'no system ignore startupconfig'
                con.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ignore startup config on {device.name}. Error:\n{e}")

def configure_interfaces_uplink(device, interfaces):
    """Configure the listed interfaces as uplinks on the device.
        Args:
            device ('obj'): Device object.
            interfaces (List['string']): List of interfaces to configure as uplinks.
    """
    config_cmd = []

    # Ensure interfaces is a list
    if not isinstance(interfaces, list):
        interfaces = [interfaces]

    for interface in interfaces:
        config_cmd.extend([
            f"interface {interface}",
            "uplink"
        ])

    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        logger.error('Failed to enable uplink interfaces on device {}: {}'.format(device.name, e))

def configure_interfaces_no_uplink(device, interfaces):
    """Configure the listed interfaces as no uplinks on the device.
        Args:
            device ('obj'): Device object.
            interfaces (List['string']): List of interfaces to configure as no uplinks.
    """
    config_cmd = []

    # Ensure interfaces is a list
    if not isinstance(interfaces, list):
        interfaces = [interfaces]

    for interface in interfaces:
        config_cmd.extend([
            f"interface {interface}",
            "no uplink"
        ])

    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        logger.error('Failed to disable uplink interfaces on device {}: {}'.format(device.name, e))
