"""Common clear functions"""
import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_controllers_ethernet_controller(device, interface=None):
    """ API to clear controllers ethernet-controller
        Args:
            device ('obj'): Device object
            interface ('str', Optional): Interface name to clear controllers
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Clear controllers ethernet-controller on {device}".format(device=device))
    cmd = 'clear controllers ethernet-controller'
    if interface:
        cmd += f' {interface}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear controllers ethernet-controller on {device}. Error:\n{error}".format(device=device, error=e)
        )
