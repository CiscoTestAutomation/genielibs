"""Common configure functions for stackwise-virtual"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

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

def unconfigure_stackwise_virtual_interfaces(device, svl_links, timeout=60):
    """ Disable global stackwise-virtual on target device
        Args:
            device ('obj'): Device object
            timeout ('int',optional): Max time for command execution
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
    # Single command 'no stackwise-virtual' will remove configuration'
    dialog = Dialog([
        Statement(
        pattern=r"WARNING\: Unconfiguring last active port\, this may result in stack-split\. Are you sure\? \[yes\/no\]\:",
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)
        ])
    command_list = []
    for interface, link_id in svl_links.items():
        command_list.append(f'interface {interface}')
        command_list.append(f'no stackwise-virtual link {link_id}')
    try:
       output = device.configure(
                command_list,
                reply=dialog,
                timeout=timeout,
                append_error_pattern=['.*Command cannot be executed.*'])
    except SubCommandFailure:
        raise SubCommandFailure('Failed to unconfigure stackwise-virtual interfaces')
    
def configure_stackwise_virtual_dual_active_interfaces(device, dad_links):
    """ Enables interface as dual-active-detection interface on target device
        Args:
            device ('obj'): Device object
            dad_links ('list'): List object
                List contains following values: interface ('str'): Interface Name
                Example:
                    dad_links = ['HundredGigE1/0/1', 'HundredGigE1/0/2']
        Returns:
            output: return the chunk of lines for the config of dual-active-detection as below..
            # interface HundredGigE1/0/1
            # stackwise-virtual dual-active-detection
        Raises:
            SubCommandFailure
    """
    # build a list of commands to send
    command_list = []
    output = ''
    for interface in dad_links:
        command_list.append(f'interface {interface}')
        command_list.append(f'stackwise-virtual dual-active-detection')
    try:
        output = device.configure(command_list)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to configure stackwise-virtual dual-active-detection interfaces')
    return output

def unconfigure_stackwise_virtual_dual_active_interfaces(device, dad_links):
    """ Disables interface as dual-active-detection interface on target device
        Args:
            device ('obj'): Device object
            dad_links ('list'): List object
                List contains following values: interface ('str'): Interface Name
                Example:
                    dad_links = ['HundredGigE1/0/1', 'HundredGigE1/0/2']
        Returns:
            output: return the chunk of lines for the config of dual-active-detection as below..
            # interface HundredGigE1/0/1
            # no stackwise-virtual dual-active-detection
        Raises:
            SubCommandFailure
    """
    # build a list of commands to send
    command_list = []
    output = ''
    for interface in dad_links:
        command_list.append(f'interface {interface}')
        command_list.append(f'no stackwise-virtual dual-active-detection')
    try:
        output = device.configure(command_list)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to unconfigure stackwise-virtual dual-active-detection interfaces')
    return output

def configure_global_dual_active_recovery_reload_disable(device):
    """ Enables global stackwise-virtual dual-active recovery reload on target device
        Args:
            device ('obj'): Device object
        Returns:
            output: return the chunk of lines for the config of pagp as below..
            # stackwise-virtual
            # Please reload the switch for Stackwise Virtual configuration to take effect
            # Upon reboot, the config will be part of running config but not part of start up config.
            # dual-active recovery-reload-disable
        Raises:
            SubCommandFailure
    """
    # build a list of commands to send
    # Add stackwise-virtual as first element in the list
    # Disables dual-active recovery-reload
    command_list = ['stackwise-virtual']
    command_list.append(f'dual-active recovery-reload-disable')
    try:
        output = device.configure(command_list)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to Enable global stackwise-virtual dual-active recovery-reload')
    return output

def unconfigure_global_dual_active_recovery_reload_disable(device):
    """ Enables global stackwise-virtual dual-active recovery reload on target device
        Args:
            device ('obj'): Device object
        Returns:
                output: return the chunk of lines for the config of pagp as below..

            # stackwise-virtual
            # Please reload the switch for Stackwise Virtual configuration to take effect
            # Upon reboot, the config will be part of running config but not part of start up config.
            # no dual-active recovery-reload-disable
        Raises:
            SubCommandFailure
    """
    # build a list of commands to send
    # Add stackwise-virtual as first element in the list
    # Enables dual-active recovery-reload
    command_list = ['stackwise-virtual']
    command_list.append(f'no dual-active recovery-reload-disable')
    try:
        output = device.configure(command_list)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to Disable global stackwise-virtual dual-active recovery-reload')
    return output

def configure_stackwise_virtual_dual_active_pagp(device, port_channel):
    """ Enables port-channel interface as pagp dual-active-detection interface on target device
        Args:
            device ('obj'): Device object
            port_channel ('str'): Port channel Value to be configured as dual-active-detection interface.

        Returns:
            output: return the chunk of lines for the config of pagp as below..
            # stackwise-virtual
            # Please reload the switch for Stackwise Virtual configuration to take effect
            # Upon reboot, the config will be part of running config but not part of start up config.
            # dual-active detection pagp
            # dual-active detection pagp trust channel-group 1     
            # Trusted port-channel 1 is not administratively down. To change the pagp dual-active trust configuration, "shutdown" the port-channel first. Remember to "no shutdown" the port-channel afterwards.
        Raises:
            SubCommandFailure
    """
    # build a list of commands to send
    command_list = ['stackwise-virtual']
    command_list.append(f'dual-active detection pagp')
    if port_channel:
        command_list.append(f'dual-active detection pagp trust channel-group {port_channel}')
    try:
        output = device.configure(command_list)    
    except SubCommandFailure:
        raise SubCommandFailure('Failed to configure a port-channel interface as stackwise-virtual dual-active-detection pagp interfaces')
    return output

def unconfigure_stackwise_virtual_dual_active_pagp(device, port_channel):
    """ Disables port-channel interface as pagp dual-active-detection interface on target device
        Args:
            device ('obj'): Device object
            port_channel ('str'): Port channel Value to be configured as dual-active-detection interface.

        Returns:
            output: return the chunk of lines for the unconfig of pagp as below..
            # stackwise-virtual 
            # Please reload the switch for Stackwise Virtual configuration to take effect
            # Upon reboot, the config will be part of running config but not part of start up config.
            # no dual-active detection pagp trust channel-group 1  
            # No dual-active trust configuration for port-channel 1
        Raises:
            SubCommandFailure
    """
    # build a list of commands to send
    command_list = ['stackwise-virtual']
    if port_channel:
        command_list.append(f'no dual-active detection pagp trust channel-group {port_channel}')
    try:
        output = device.configure(command_list)    
    except SubCommandFailure:
        raise SubCommandFailure('Failed to unconfigure a port-channel interface as stackwise-virtual dual-active-detection pagp interfaces')
    return output
