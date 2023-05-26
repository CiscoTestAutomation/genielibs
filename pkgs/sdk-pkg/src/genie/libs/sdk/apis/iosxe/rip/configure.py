"""Common configure functions for rip"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def unconfigure_ripng(device, pid):
    """unconfigure ripng
        Args:
            device ('obj'): Device object
            pid ('str'): ripng process id
        Return:
            None
        Raises:
            SubCommandFailure
    """
    log.info("unconfigure  RIPng configuration on {hostname}")
    config = 'no ipv6 router rip {pid}'.format(pid=pid)
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "RIPng is not unconfigured on device"
            " {device}, Error: {error}".format(
               device=device.name, error=e))
        
def configure_ripng(device, pid):
    """unconfigure ripng
        Args:
            device ('obj'): Device object
            pid ('str'): ripng process id
        Return:
            None
        Raises:
            SubCommandFailure
    """
    log.info("configure  RIPng configuration on {hostname}")
    config = 'ipv6 router rip {pid}'.format(pid=pid)
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "RIPng is not configured on device"
            " {device}, Error: {error}".format(
               device=device.name, error=e))
        
def unconfigure_rip(device):
    """unconfigure rip
        Args:
            device ('obj'): Device object
        Return:
            None
        Raises:
            SubCommandFailure
    """
    log.info("unconfigure  RIP configuration on {hostname}")
    config = 'no router rip'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "RIP is not unconfigured on device"
            " {device}, Error: {error}".format(
               device=device.name, error=e))
        
def config_interface_ripng(device, interface, pid):
    """config RIPng on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            ripng_pid ('str'): ripng process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring RIPng on interface {interface}".format(interface=interface))
    config = ['interface {interface}'.format(interface=interface),
              'ipv6 rip {pid} enable'.format(pid=pid)]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ripng {pid} on interface. Error:\n{error}"
            .format(pid=pid, error=e))
        
def unconfig_interface_ripng(device, interface, pid):
    """unconfig RIPng on interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            ripng_pid ('str'): ripng process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Unconfiguring RIPng on interface {interface}".format(interface=interface))
    config = ['interface {interface}'.format(interface=interface),
              'no ipv6 rip {pid} enable'.format(pid=pid)]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure ripng {pid} on interface. Error:\n{error}"
            .format(pid=pid, error=e))
    
def configure_rip(device, network):
    """configure rip
        Args:
            device ('obj'): Device object
            network ('str'): network address
        Return:
            None
        Raises:
            SubCommandFailure
    """
    log.info("unconfigure  RIP configuration on {hostname}")
    
    config = ['router rip',
              'network {network}'.format(network=network)]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "RIP is not unconfigured on device"
            " {device}, Error: {error}".format(
               device=device.name, error=e))

def clear_ipv6_rip(device):
    """ clear ipv6 rip
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear ipv6 rip on {device}".format(device=device))
    config = 'clear ipv6 rip'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ipv6 rip on {device}. Error:\n{error}".format(device=device, error=e)
        )
