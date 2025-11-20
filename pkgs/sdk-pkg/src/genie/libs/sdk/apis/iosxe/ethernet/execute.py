"""Execute functions for ethernet CFM (Connectivity Fault Management)"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)


def execute_show_ethernet_cfm_maintenance_points_remote(device):
    """ Execute 'show ethernet cfm maintenance-points remote'

        Args:
            device ('obj'): Device object

        Returns:
            str: Command output

        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd = "show ethernet cfm maintenance-points remote"
    
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to execute '{cmd}' on {device.name}")
        raise SubCommandFailure(
            f"Could not execute '{cmd}' on {device.name}. Error:\n{e}"
        )
    
    return output


def execute_show_ethernet_cfm_maintenance_points_local(device):
    """ Execute 'show ethernet cfm maintenance-points local'

        Args:
            device ('obj'): Device object

        Returns:
            str: Command output

        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd = "show ethernet cfm maintenance-points local"
    
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to execute '{cmd}' on {device.name}")
        raise SubCommandFailure(
            f"Could not execute '{cmd}' on {device.name}. Error:\n{e}"
        )
    
    return output


def execute_show_ethernet_cfm_errors(device):
    """ Execute 'show ethernet cfm errors'

        Args:
            device ('obj'): Device object

        Returns:
            str: Command output

        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd = "show ethernet cfm errors"
    
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to execute '{cmd}' on {device.name}")
        raise SubCommandFailure(
            f"Could not execute '{cmd}' on {device.name}. Error:\n{e}"
        )
    
    return output