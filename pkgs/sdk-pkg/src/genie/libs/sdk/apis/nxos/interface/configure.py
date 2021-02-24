import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_interfaces_shutdown(device, interfaces):
    """ Shutdown the listed interfaces in the given list on the device

        Args:
            List['string']: Interfaces to shutdown
            device ('obj'): Device object
    """
    config_cmd = []
    for interface in interfaces:
        config_cmd += ["interface {interface}".format(interface=interface), "shutdown"]
    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        log.error('Failed to shutdown interfaces on device {}: {}'.format(device.name, e))

def configure_interfaces_unshutdown(device, interfaces):
    """ Enable the listed interfaces in the given list on the device

        Args:
            List['string']: Interfaces to enable
            device ('obj'): Device object
    """
    config_cmd = []
    for interface in interfaces:
        config_cmd += ["interface {interface}".format(interface=interface), "no shutdown"]
    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        log.error('Failed to enable interfaces on device {}: {}'.format(device.name, e))