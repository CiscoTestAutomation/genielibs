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

def configure_ipv6_nd_cache_expire(device, timeout):
    """ Configure ipv6 nd cache expire timeout
        Args:
            device (`obj`): Device object
            timeout ('int') : time need to set to expire cache        
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'ipv6 nd cache expire {timeout}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 nd cache expire timeout on {device}. Error:\n{e}")

def unconfigure_ipv6_nd_cache_expire(device):
    """ Unconfigure ipv6 nd cache expire
        Args:
            device (`obj`): Device object       
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure('no ipv6 nd cache expire')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 nd cache expire on {device}. Error:\n{e}")

def configure_ipv6_flow_monitor_sampler(device, interface, monitor_name=None, sampler_name=None):
    """ Configure IPv6 flow monitor sampler on the specified interface.
        Args:
            device (obj): Device object
            interface (str): Interface name
            monitor_name (str): The flow monitor name
            sampler_name (str): The sampler name
        Returns:
            None
        Raises:
            SubCommandFailure:
    """
    cmd = [
        f"interface {interface}",  
        f"ipv6 flow monitor {monitor_name} sampler {sampler_name} input",
        "end"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to configure IPv6 flow monitor sampler on {interface}. Error: {e}")
        raise SubCommandFailure(
            f"Could not configure IPv6 flow monitor sampler on {device} for {interface}. Error:\n{e}"
        )

def unconfigure_ipv6_dhcp_pool_prefix_delegation_pool(device, pool_name, prefix_pool_name):
    """ unconfigure ipv6 dhcp pool prefix delegation pool
        Args:
            device ('obj')    : device to use
            pool_name ('str') : DHCP pool name
            prefix_pool_name ('str'): IPv6 Prefix pool name.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'ipv6 dhcp pool {pool_name}', f'no prefix-delegation pool {prefix_pool_name}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ipv6 dhcp pool prefix delegation pool:\n{e}")

def unconfigure_ipv6_local_pool(device, name):
    """ Unconfigure ip6 local pool
        Args:
            device (`obj`): Device object
            name ('str') : Name of local prefix pool
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'no ipv6 local pool {name}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 local pool on {device}. Error:\n{e}")
