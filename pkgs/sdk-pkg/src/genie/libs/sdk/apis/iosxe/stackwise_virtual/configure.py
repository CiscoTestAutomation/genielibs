"""Common configure functions for stackwise-virtual"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_global_stackwise_virtual(device, domain=None):
    """ Enables global stackwise-virtual on target device
        Args:
            device ('obj'): Device object
            domain ('str'): Stackwise-virtual domain
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # build a list of commands to send
    # Add stackwise-virtual as first element in the list
    # Add domain only if domain argument has been provided
    command_list = ['stackwise-virtual']
    if domain:
        command_list.append(f'domain {domain}')
    try:
        output = device.configure(command_list)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to configure global stackwise-virtual')
    return output

def unconfigure_global_stackwise_virtual(device):
    """ Disable global stackwise-virtual on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # Single command 'no stackwise-virtual' will remove configuration
    command = 'no stackwise-virtual'
    try:
        output = device.configure(command)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to remove global stackwise-virtual')
    return output

def configure_stackwise_virtual_interfaces(device, svl_links):
    """ Enables global stackwise-virtual on target device
        Args:
            device ('obj'): Device object
            svl_links ('dict'): Dict object
                Dictionary contains following key, values:
                    key: interface ('str'): Interface Name
                    value: link_id ('str'): SVL link id
                Example:
                    svl_links = {
                        'HundredGigE1/0/1':'1',
                        'HundredGigE1/0/2':'1'
                    }
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # build a list of commands to send
    # Add stackwise-virtual as first element in the list
    # Add domain only if domain argument has been provided
    command_list = []
    for interface, link_id in svl_links.items():
        command_list.append(f'interface {interface}')
        command_list.append(f'stackwise-virtual link {link_id}')
    try:
        output = device.configure(command_list)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to configure stackwise-virtual interfaces')
    return output
    
def unconfigure_stackwise_virtual_interfaces(device, svl_links):
    """ Disable global stackwise-virtual on target device
        Args:
            device ('obj'): Device object
            svl_links ('dict'): Dict object
                Dictionary contains following key, values:
                    key: interface ('str'): Interface Name
                    value: link_id ('str'): SVL link id
                Example:
                    svl_links = {
                        'HundredGigE1/0/1':'1',
                        'HundredGigE1/0/2':'1'
                    }
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # Single command 'no stackwise-virtual' will remove configuration
    command_list = []
    for interface, link_id in svl_links.items():
        command_list.append(f'interface {interface}')
        command_list.append(f'no stackwise-virtual link {link_id}')
    try:
        output = device.configure(command_list)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to remove stackwise-virtual interfaces')
    return output
        