"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_enable_ipv6_routing(device):
    """ configure ipv6 routing on device

        Args:
            device (`obj`): Device object
        Returns:
            None
    """
    try:
        device.configure("ipv6 unicast-routing")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configure ipv6 unicast-routing. Error {e}".format(e=e)
        )


def unconfig_disable_ipv6_routing(device):
    """Unconfigure ipv6 unicast-routing on the device
    
       Args:
            device('obj'): Device object

       Returns:
            None

       Raises:
            SubCommandFailure     
    
    """

    try:
        device.configure("no ipv6 unicast-routing")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ipv6 unicast routing")


def configure_ipv6_dhcp_pool_preifx_delegation_pool(device, pool_name, prefix_pool_name, start_lifetime=False,
                                                    end_lifetime=None):
    """ configure ipv6 dhcp pool prefix delegation pool
        Args:
            device ('obj')    : device to use
            pool_name ('str') : DHCP pool name
            prefix_pool_name ('str'): IPv6 Prefix pool name.
            start_lifetime ('str', optional): Valid start time. Default is None.
            end_lifetime ('str', optional): Valid end time. Default is None.
        Returns:
            None
        Raises:
            SubCommandFailure    
    """
    cmd = [f'ipv6 dhcp pool {pool_name}']
    if start_lifetime and end_lifetime:
        cmd.append(f'prefix-delegation pool {prefix_pool_name} lifetime {start_lifetime} {end_lifetime}')
    else:
        cmd.append(f'prefix-delegation pool {prefix_pool_name}')
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 dhcp pool prefix delegation pool:\n{e}")


def configure_ipv6_local(device, route_map_name=None, prefix_pool_name=None, ipv6_pool_prefix=None,
                         prefix_from_pool=None, cache_size=None, shared=False):
    """ configure ipv6 local pool or policy
        Args:
            device ('obj')    : device to use
            route_map_name ('str', optional) : Route map name. Default is None.
            prefix_pool_name ('str', optional): IPv6 Prefix pool name. Default is None.
            ipv6_pool_prefix ('str', optional): IPv6 pool prefix ex: ::1/64. Default is None.
            prefix_from_pool ('str', optional): Prefix length to assign from pool. Default is None.
            cache_size ('str', optional): Number of free entries to search. Default is None.
            shared ('str', optional): Advertise the same prefix. Default is False.
        Returns:
            None
        Raises:
            SubCommandFailure    
    """
    cmd = []
    if route_map_name:
        cmd.append(f'ipv6 local policy route-map {route_map_name}')
    elif prefix_pool_name and ipv6_pool_prefix and prefix_from_pool:
        command = f'ipv6 local pool {prefix_pool_name} {ipv6_pool_prefix} {prefix_from_pool}'
        if shared:
            command += ' shared'
        if cache_size:
            command += f' cache-size {cache_size}'
        cmd.append(command)

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipv6 local pool or policy:\n{e}")

def configure_ipv6_local_pool(device, name, pool_prefix, prefix_length):
    """ Configure ip6 local pool
        Args:
            device (`obj`): Device object
            name ('str') : Name of local prefix pool
            pool_prefix ('str') : IPv6 pool prefix (X:X:X:X::X/<0-128>)
            prefix_length ('str') : Prefix length to assign from pool       
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f'ipv6 local pool {name} {pool_prefix} {prefix_length}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 local pool on {device}. Error:\n{e}")
