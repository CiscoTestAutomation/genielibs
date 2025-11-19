# Python
import logging

# genie
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_ip as _configure_management_ip

# Unicon
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)

def configure_ignore_startup_config(device):
    """  To configure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure the device
    """

    try:
        # If the device state is in rommon configure rommon variable
        if device.state_machine.current_state == 'rommon':
            cmd = 'confreg 0x2142'
            device.execute(cmd)
        else:
            cmd = 'config-register 0x2142'
            device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ignore startup config on {device.name}. Error:\n{e}")

def unconfigure_ignore_startup_config(device):
    """ To unconfigure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to unconfigure the device
    """
    
    try:
        # If the device state is in rommon configure rommon variable
        if device.state_machine.current_state == 'rommon':
            cmd = 'confreg 0x2102'
            device.execute(cmd)
        else:
            cmd = 'config-register 0x2102'
            device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ignore startup config on {device.name}. Error:\n{e}")

def configure_management_ip(device,
                            address=None,
                            interface=None,
                            vrf=None,
                            no_switchport=True,
                            dhcp_timeout=30):
    '''
    Configure management ip on the device.
    Args:
        device ('obj'):  device object
        address ('dict'):  Address(es) to configure on the device (syntax: address/mask) (optional)
             ipv4 ('str') or ('list'): ipv4 address
             ipv6 ('str') or ('list'): ipv6 address
        interface ('str'): management interface (optional)
        vrf ('str'): interface VRF (optional)
        no_switchport ('bool'): default as True
        dchp_timeout ('int'): DHCP timeout in seconds (default: 30)
    Returns:
        None
    Examples:
        # Configure IP on interface
        device.api.configure_management_ip(interface='GigabitEthernet0', address={'ipv4': '1.1.1.1/24'})
        # Use config details from device in testbed
        #
        # R1:
        #   management:
        #     interface: GigabitEthernet0
        #     address:
        #        ipv4: '1.1.1.1/24'
        #        ipv6: '2001::123/64'
        # api picks up ip from testbed
        device.api.configure_management_ip()
        # IPv6 management address in a VRF
        device.api.configure_management_ip(interface='GigabitEthernet0', address={'ipv6': '2001::123/64'}, vrf='Mgmt-vrf')
        # Multiple addresses
        device.api.configure_management_ip(interface='GigabitEthernet0', address={'ipv4': ['1.1.1.1/24'], 'ipv6': ['2001::123/64']})
        # no switchport
        device.api.configure_management_ip(interface='GigabitEthernet0', address={'ipv6': '2001::123/64'}, no_switchport=True)
        # The api also supports the ipv4/ipv6 dhcp and ipv6/autoconfig.
        # Use config details from device in testbed
        # Example 1: (ipv4/ipv6 dhcp)
        # R1:
        #   management:
        #     interface: GigabitEthernet0
        #     address:
        #        ipv4: 'ipv4/dhcp'
        #        ipv6: 'ipv6/dhcp'
        #
        # Example 2: (ipv6 autoconfig)
        # R1:
        #   management:
        #     interface: GigabitEthernet0
        #     address:
        #        ipv6: 'ipv6/autoconfig'
        # api picks up ip from testbed
        device.api.configure_management_ip()
    '''
    _configure_management_ip(device=device,
                             address=address,
                             interface=interface,
                             vrf=vrf,
                             no_switchport=no_switchport,
                             dhcp_timeout=dhcp_timeout)


def configure_autoboot(device):
    """ Configure autoboot
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = 'config-reg 0x2102'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure Autoboot on c9800 device. Error:\n{e}')