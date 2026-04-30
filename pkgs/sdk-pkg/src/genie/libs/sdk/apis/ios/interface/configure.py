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
        config_cmd = ["int {interface}".format(interface=interface), "shutdown"]
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
        config_cmd = ["int {interface}".format(interface=interface), "no shutdown"]
    try:
        device.configure(config_cmd)
    except SubCommandFailure as e:
        log.error('Failed to enable interfaces on device {}: {}'.format(device.name, e))


def configure_interface(device, interface, ip_address=None, mask=None,
                        ipv6_address=None, ipv6_prefix_length=None,
                        mac_address=None, ipv6_enable=False, shutdown=False,
                        dhcp=None, ipv6_autoconfig=None):
    """ Configure interface with optional IPv4/IPv6 address and settings

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name (e.g. 'GigabitEthernet0/0')
            ip_address (`str`, optional): IPv4 address. Defaults to None
            mask (`str`, optional): IPv4 subnet mask. Defaults to None
            ipv6_address (`str`, optional): IPv6 address. Defaults to None
            ipv6_prefix_length (`str`, optional): IPv6 prefix length (e.g. '64'). Defaults to None
            mac_address (`str`, optional): MAC address to set. Defaults to None
            ipv6_enable (`bool`, optional): Enable IPv6 on interface. Defaults to False
            shutdown (`bool`, optional): If False, sends 'no shutdown'. Defaults to False
            dhcp (`str`, optional): If set, sends 'ip address dhcp'. Defaults to None
            ipv6_autoconfig (`str`, optional): If set, sends 'ipv6 address autoconfig'.
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if mac_address:
        cmd.append(f" mac-address {mac_address}")
    if not shutdown:
        cmd.append(" no shutdown")
    if ipv6_enable:
        cmd.append(" ipv6 enable")
    if dhcp:
        cmd.append(f" ip address {dhcp}")
    elif ip_address and mask:
        cmd.append(f" ip address {ip_address} {mask}")
    if ipv6_autoconfig:
        cmd.append(f" ipv6 address {ipv6_autoconfig}")
    elif ipv6_address and ipv6_prefix_length:
        cmd.append(f" ipv6 address {ipv6_address}/{ipv6_prefix_length}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure interface {interface}. Error: {e}"
        )


def unconfigure_interface(device, interface, ip_address=None, mask=None,
                          ipv6_address=None, ipv6_prefix_length=None,
                          mac_address=None, ipv6_enable=False, shutdown=True,
                          dhcp=None, ipv6_autoconfig=None):
    """ Unconfigure interface settings

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name (e.g. 'GigabitEthernet0/0')
            ip_address (`str`, optional): IPv4 address to remove. Defaults to None
            mask (`str`, optional): IPv4 subnet mask. Defaults to None
            ipv6_address (`str`, optional): IPv6 address to remove. Defaults to None
            ipv6_prefix_length (`str`, optional): IPv6 prefix length. Defaults to None
            mac_address (`str`, optional): MAC address to remove. Defaults to None
            ipv6_enable (`bool`, optional): Disable IPv6 on interface. Defaults to False
            shutdown (`bool`, optional): If True, sends 'shutdown'. Defaults to True
            dhcp (`str`, optional): If set, sends 'no ip address dhcp'. Defaults to None
            ipv6_autoconfig (`str`, optional): If set, sends 'no ipv6 address autoconfig'.
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if mac_address:
        cmd.append(f" no mac-address {mac_address}")
    if shutdown:
        cmd.append(" shutdown")
    if ipv6_enable:
        cmd.append(" no ipv6 enable")
    if dhcp:
        cmd.append(f" no ip address {dhcp}")
    elif ip_address and mask:
        cmd.append(f" no ip address {ip_address} {mask}")
    if ipv6_autoconfig:
        cmd.append(f" no ipv6 address {ipv6_autoconfig}")
    elif ipv6_address and ipv6_prefix_length:
        cmd.append(f" no ipv6 address {ipv6_address}/{ipv6_prefix_length}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure interface {interface}. Error: {e}"
        )


def configure_interface_ipv6_nd(device, interface, ns_interval=None,
                                dad_attempts=None, ipv6_enable=False,
                                keepalive=False, shutdown=False):
    """ Configure interface IPv6 Neighbor Discovery settings

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name (e.g. 'GigabitEthernet0/0')
            ns_interval (`int`, optional): NS interval in milliseconds. Defaults to None
            dad_attempts (`int`, optional): DAD attempts count. Defaults to None
            ipv6_enable (`bool`, optional): Enable IPv6 on interface. Defaults to False
            keepalive (`bool`, optional): If False, sends 'no keepalive'. Defaults to False
            shutdown (`bool`, optional): If False, sends 'no shutdown'. Defaults to False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if ipv6_enable:
        cmd.append(" ipv6 enable")
    if ns_interval is not None:
        cmd.append(f" ipv6 nd ns-interval {ns_interval}")
    if dad_attempts is not None:
        cmd.append(f" ipv6 nd dad attempts {dad_attempts}")
    if not shutdown:
        cmd.append(" no shutdown")
    if not keepalive:
        cmd.append(" no keepalive")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure interface {interface} ipv6 nd. Error: {e}"
        )


def unconfigure_interface_ipv6_nd(device, interface, ns_interval=None,
                                  dad_attempts=None, ipv6_enable=False,
                                  keepalive=True, shutdown=True):
    """ Unconfigure interface IPv6 Neighbor Discovery settings

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name (e.g. 'GigabitEthernet0/0')
            ns_interval (`int`, optional): NS interval to remove. Defaults to None
            dad_attempts (`int`, optional): DAD attempts to remove. Defaults to None
            ipv6_enable (`bool`, optional): Disable IPv6 on interface. Defaults to False
            keepalive (`bool`, optional): If True, restores keepalive. Defaults to True
            shutdown (`bool`, optional): If True, sends 'shutdown'. Defaults to True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if ipv6_enable:
        cmd.append(" no ipv6 enable")
    if ns_interval is not None:
        cmd.append(f" no ipv6 nd ns-interval {ns_interval}")
    if dad_attempts is not None:
        cmd.append(f" no ipv6 nd dad attempts {dad_attempts}")
    if shutdown:
        cmd.append(" shutdown")
    if keepalive:
        cmd.append(" keepalive")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure interface {interface} ipv6 nd. Error: {e}"
        )