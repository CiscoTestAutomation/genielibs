"""Common configure functions for LACP"""

import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_lacp_ratefast(device, interface):
    """configure lacp rate fast on a interface
        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('lacp rate fast')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure lacp rate fast on interface {interface}. Error:\n{e}")

def unconfigure_lacp_ratefast(device, interface):
    """unconfigure lacp rate fast on a interface
        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no lacp rate fast')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure lacp rate fast on interface {interface}. Error:\n{e}")

def configure_lacp_port_priority(device, interface, priority):
    """configure lacp port-priority on a interface
        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
            priority (`int`): port priority <0-65535>
        Return:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append(f'lacp port-priority {priority}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure lacp port-priority on interface {interface}. Error:\n{e}")

def unconfigure_lacp_port_priority(device, interface):
    """unconfigure lacp port-priority on a interface
        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    cmd.append(f'interface {interface}')
    cmd.append('no lacp port-priority')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure lacp port-priority on interface {interface}. Error:\n{e}")

def configure_lacp_system_priority(device, priority):
    """ configure lacp system-priority on a interface

        Args:
            device (`obj`): Device object
            priority (`int`): system priority <0-65535>

        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = (f'lacp system-priority {priority}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure lacp system-priority. Error:\n{e}")

def unconfigure_lacp_system_priority(device):
    """ unconfigure lacp system-priority on a interface

        Args:
            device (`obj`): Device object

        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = 'no lacp system-priority' 
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure lacp system-priority. Error:\n{e}")

def configure_port_channel_mode(device, mode, lb_method=None):
    """ configure port channel mode

        Args:
            device (`obj`): Device object
            mode (`str`): port-channel mode auto/load-balance
            lb_method(`str'): portchannel load balance method 
            ex.)    
                    dst-ip                 Dst IP Addr
                    dst-mac                Dst Mac Addr
                    dst-mixed-ip-port      Dst IP Addr and TCP/UDP Port
                    dst-port               Dst TCP/UDP Port
                    extended               Extended Load Balance Methods
                    src-dst-ip             Src XOR Dst IP Addr
                    src-dst-mac            Src XOR Dst Mac Addr
                    src-dst-mixed-ip-port  Src XOR Dst IP Addr and TCP/UDP Port
                    src-dst-port           Src XOR Dst TCP/UDP Port
                    src-ip                 Src IP Addr
                    src-mac                Src Mac Addr
                    src-mixed-ip-port      Src IP Addr and TCP/UDP Port
                    src-port               Src TCP/UDP Port

        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if mode.lower() == "auto":
        cmd.append("port-channel auto")
    if mode.lower() == "load-balance":
        cmd.append(f'port-channel load-balance {lb_method}')

    cmd
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure port channel mode. Error:\n{e}")

def unconfigure_port_channel_mode(device, mode):
    """ unconfigure port channel mode

        Args:
            device (`obj`): Device object
            mode (`str`): port-channel mode auto/load-balance

        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'no port-channel {mode}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure port channel mode. Error:\n{e}")


def clear_lacp_counters(device, channel_group=None):
    """ clear lacp counters

        Args:
            device ('obj'): Device object
            channel_group ('int', optional): Channel group number. Default is None

        Return:
            None
        Raises:
            SubCommandFailure
    """
    if channel_group:
        cmd = f'clear lacp {channel_group} counters'
    else:
        cmd = f'clear lacp counters'

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to clear lacp counters. Error:\n{e}")
