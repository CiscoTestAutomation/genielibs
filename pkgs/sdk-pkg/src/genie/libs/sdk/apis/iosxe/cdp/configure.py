"""Common configure functions for cdp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_cdp(device, interfaces=None):
    """ Enables cdp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    interface_list = {}
    # if no list of interfaces given get list of all interfaces
    if interfaces is None:
        interface_list = device.parse('show interfaces')
    else:
        interface_list = device.api.get_interface_information(interface_list)
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

def unconfigure_cdp(device, interfaces=None):
    """ Disable cdp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    interface_list = {}
    # if no list of interfaces given get list of all interfaces
    if interfaces is None:
        interface_list = device.parse('show interfaces')
    else:
        interface_list = device.api.get_interface_information(interface_list)
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