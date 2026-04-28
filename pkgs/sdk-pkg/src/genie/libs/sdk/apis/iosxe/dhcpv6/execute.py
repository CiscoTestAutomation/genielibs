"""Execute DHCP related command"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def clear_ipv6_dhcp_conflict(device):
    """execute 'clear ipv6 dhcp conflict *' on device
       Args:
            device('obj'): device object
       Returns:
            None
       Raises:
            SubCommandFailure
    """
    log.debug("Executing clear_ipv6_dhcp_conflict API")
    try:
        device.execute("clear ipv6 dhcp conflict *")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear ipv6 dhcp conflict\n{e}'
        )


def execute_show_ipv6_dhcp_interface(device, interface, filter=None):
    """ Execute 'show ipv6 dhcp interface {interface}'

        Args:
            device ('obj'): Device object
            interface ('str'): Interface name (e.g. GigabitEthernet0/0/0)
            filter ('str', optional): filter option to append (e.g. 'include Address'). Default is None

        Returns:
            str: Command output

        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd = f"show ipv6 dhcp interface {interface}"
    if filter:
        cmd += f" | {filter}"

    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to execute '{cmd}' on {device.name}")
        raise SubCommandFailure(
            f"Could not execute '{cmd}' on {device.name}. Error:\n{e}"
        )

    return output


def execute_show_ipv6_dhcp_interface_all(device, filter=None):
    """ Execute 'show ipv6 dhcp interface'

        Args:
            device ('obj'): Device object
            filter ('str', optional): filter option to append (e.g. 'include Address'). Default is None

        Returns:
            str: Command output

        Raises:
            SubCommandFailure: Failed executing command
    """
    cmd = "show ipv6 dhcp interface"
    if filter:
        cmd += f" | {filter}"

    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to execute '{cmd}' on {device.name}")
        raise SubCommandFailure(
            f"Could not execute '{cmd}' on {device.name}. Error:\n{e}"
        )

    return output