"""Common configure functions for cdp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_cdp(device, interfaces=None, timeout=300):
    """ Enables cdp on target device
        Args:
            device ('obj'): Device object
            interfaces ('list', optional): List of interfaces. Default is None
            timeout ('int', optional): Timeout value for show interfaces parser. Default is 300 seconds
        Returns:
            None
    """
    interface_list = {}
    # if no list of interfaces given get list of all interfaces
    if interfaces is None:
        interface_list = device.parse('show interfaces', timeout=timeout)
    else:
        interface_list = device.api.get_interface_information(interfaces)
    skipped_ints = []

    # build a list of commands to send, checks if interface is correct type
    # before adding to command list
    command_list = ['cdp run']
    for interface in interface_list:
        if interface_list[interface]['type'] in ['Loopback','Tunnel', 'GEChannel']:
            skipped_ints.append(interface)
            continue
        command_list.append('interface ' + interface)
        command_list.append('cdp enable')

    # log which interfaces were skipped and then run command
    if skipped_ints:
        log.info('Skipped interfaces {} due to type incompatability'.format(skipped_ints))
    device.configure(command_list)

def unconfigure_cdp(device, interfaces=None, timeout=300):
    """ Disable cdp on target device
        Args:
            device ('obj'): Device object
            interfaces ('list', optional): List of interfaces. Default is None
            timeout ('int', optional): Timeout value for show interfaces parser. Default is 300 seconds
        Returns:
            None
    """
    interface_list = {}
    # if no list of interfaces given get list of all interfaces
    if interfaces is None:
        interface_list = device.parse('show interfaces', timeout=timeout)
    else:
        interface_list = device.api.get_interface_information(interfaces)
    skipped_ints = []

    # build a list of commands to send, checks if interface is correct type
    # before adding to command list
    command_list = ['no cdp run']
    for interface in interface_list:
        if interface_list[interface]['type'] in ['Loopback','Tunnel', 'GEChannel']:
            skipped_ints.append(interface)
            continue
        command_list.append('interface ' + interface)
        command_list.append('no cdp enable')
    
    # log which interfaces were skipped and then run command
    if skipped_ints:
        log.info('Skipped interfaces {} due to type incompatability'.format(skipped_ints))
    device.configure(command_list)

def configure_cdp_interface(device, interface):
    """ Configure CDP on interface

        Args:
            device ('obj'): Device object
            interface ('str'): interface on which CDP to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure CDP on interface")
    configs = []
    configs.append("cdp run")
    configs.append(f"interface {interface}")
    configs.append("cdp enable")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure CDP on interface"
            "Error: {error}".format(error=e)
            )

def unconfigure_cdp_interface(device, interface):
    """ Unconfigure CDP on interface

        Args:
            device ('obj'): Device object
            interface ('str'): interface on which CDP to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unonfigure CDP on interface")
    configs = []
    configs.append(f"interface {interface}")
    configs.append("no cdp enable")
    configs.append("no cdp run")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure CDP on interface"
            "Error: {error}".format(error=e)
            )

def configure_cdp_neighbors(device):
    """ Enables cdp on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    command_list = ['cdp run']
    try:
        device.configure(command_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure CDP Globally"
            "Error: {error}".format(error=e)
        )

def unconfigure_cdp_neighbors(device):
    """ Disable cdp on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """ 
    command_list = ['no cdp run']
    try:
        device.configure(command_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure CDP Globally"
            "Error: {error}".format(error=e)
        )

def configure_cdp_timer(device, timer):
    """ Configure cdp timer on target device globally on the device
        Args:
            device ('obj'): Device object
            timer ('int'): CDP timer in seconds between 5-254 seconds
        Returns:
            None
    """
    command_list = [f'cdp timer {timer}']
    try:
        device.configure(command_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure CDP timer"
            "Error: {error}".format(error=e)
        )

def unconfigure_cdp_timer(device):
    """ Disable cdp timer on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """ 
    command_list = ['no cdp timer']
    try:
        device.configure(command_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure CDP timer"
            "Error: {error}".format(error=e)
        )


def configure_cdp_holdtime(device, timer):
    """ Configure cdp holdtime on target device globally on the device
        Args:
            device ('obj'): Device object
            timer ('int'): CDP holdtime in seconds between 10-255 seconds
        Returns:
            None
    """
    command_list = [f'cdp holdtime {timer}']
    try:
        device.configure(command_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure CDP holdime"
            "Error: {error}".format(error=e)
        )

def unconfigure_cdp_holdtime(device):
    """ Disable cdp holdtime on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """ 
    command_list = ['no cdp holdtime']
    try:
        device.configure(command_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure CDP holdtime"
            "Error: {error}".format(error=e)
        )
