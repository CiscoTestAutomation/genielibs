# Python
import logging
import re
from datetime import datetime

# pyats
from pyats.easypy import runtime

# genie
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_ip as _configure_management_ip
from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

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


def collect_install_log(device, timeout=600):
    """ Collect install failure logs from the device.
    Args:
        device (obj): Device object (required)
        timeout (int): timeout for show tech-support command (default: 600s)
    Returns
        None
    """

    archive_filename = None

    log.info("Logging the below to get the install failure logs from device")

    # Add timestamp to the show tech support filename
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')[:-3]
    file_name = f"show_tech_support_{timestamp}.txt"

    commands = [
        "show platform software install-manager chassis active r0 operation current detail",
        "show platform software install-manager chassis active r0 operation history detail",
    ]

    for command in commands:
        device.execute(command)

    show_tech_commands = [
        f"show tech-support install | append {file_name}"
    ]

    for command in show_tech_commands:
        device.execute(command, timeout=timeout)

    output = device.execute("request platform software trace archive", timeout=timeout)
    match = re.search(r'Done with creation of the archive file:\s*\[(.*?)\]', output)
    if match:
        archive_filename = match.group(1)

    try:
        # Get default directory to copy the files
        log.info("Getting default directory to copy the files")
        default_dir = get_default_dir(device)

        log.info(f"Copying file {file_name} to runinfo directory: {runtime.directory}")
        device.api.copy_from_device(local_path=f"{default_dir}{file_name}", remote_path=runtime.directory)
        if archive_filename:
            log.info(f"Copying archive file {archive_filename} to runinfo directory: {runtime.directory}")
            device.api.copy_from_device(local_path=f"{archive_filename}", remote_path=runtime.directory)

    except Exception as e:
        log.error(f"Failed to copy the install failure logs to runinfo directory: {e}", exc_info=True)