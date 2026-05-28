"""Common execute functions for simulator"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def execute_clear(device, command):
    """ Execute clear command on device

        Args:
            device (`obj`): Device object
            command (`str`): Command string to clear
                (e.g. 'simulator radius request all',
                 'simulator radius subscriber 1')
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute(f"clear {command}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute clear {command}. Error: {e}"
        )


def execute_simulator_radius_request_coa(device, profile_num,
                                         client_ip=None, host_ip=None):
    """ Execute simulator radius CoA request on device

        Args:
            device (`obj`): Device object
            profile_num (`int`): Profile number
            client_ip (`str`, optional): Client IP address.
                Required together with host_ip. Defaults to None
            host_ip (`str`, optional): Host IP address.
                Required together with client_ip. Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"simulator radius request 1 coa {profile_num}"
    if client_ip and host_ip:
        cmd += f" client {client_ip} host {host_ip}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute simulator radius request coa. Error: {e}"
        )
