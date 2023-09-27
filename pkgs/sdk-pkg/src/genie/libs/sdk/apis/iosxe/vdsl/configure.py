import logging
from unicon.core.errors import SubCommandFailure
from pyats.aetest.steps import Steps
from genie.conf.base import Interface

log = logging.getLogger(__name__)

def configure_controller_shutdown(device, interface, shutdown=True):
    """ Configures the shutdown/no shutdown for VDSL interface
        Args:
            device ('obj'): device to use
            interface ('str'): controller vdsl interface
            shutdown ('bool', optional) : true/false need to be send. default is false/Shutdown
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = 'shutdown' if shutdown else 'no shutdown'
    log.debug(f"Configuring VDSL interface {cmd} on device {device}")

    try:
        device.configure(
            "Controller VDSL {interface}\n"
            "{cmd}".format(interface=interface,cmd=cmd))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure controller VDSL shutdown/no shutdown. Error:\n{error}".format(error=e))


