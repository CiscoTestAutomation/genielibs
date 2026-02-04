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

def configure_ipv6_flow_monitor_sampler(device, interface, direction="input", monitor_name=None, sampler_name=None):
    """ Configure IPv6 flow monitor sampler on the specified interface.
        Args:
            device (obj): Device object
            interface (str): Interface name
            direction ('str'): Direction of monitor (input/output/both)
            monitor_name (str): The flow monitor name
            sampler_name (str): The sampler name
        Returns:
            None
        Raises:
            SubCommandFailure:
    """
    cmd = [
        f"interface {interface}",  
        f"ipv6 flow monitor {monitor_name} sampler {sampler_name} {direction}",
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

def configure_logging_ipv6(device, syslog_host, transport=None):
    """ Configure logging for an IPv6 syslog host
        Args:
            device (`obj`): Device object
            syslog_host (`str`): IPv6 address of the syslog host
            transport (`str`, optional): Transport method (e.g., "udp" or "tcp"). Default is None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []

    # Add logging host command based on conditions
    if transport:
        cmd.append(f"logging host ipv6 {syslog_host} transport {transport}")
    else:
        cmd.append(f"logging host ipv6 {syslog_host}")

    # Add logging trap level as a separate command
    cmd.append("logging trap debugging")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure logging for IPv6 syslog host {syslog_host}. Error:\n{e}"
        )

def configure_ipv6_logging_with_transport_and_facility(device, host_ip, transport_protocol, port):
    """ Configure IPv6 logging with transport and facility on the device
        Args:
            device (`obj`): Device object
            host_ip (`str`): IPv6 address of the logging host
            transport_protocol (`str`): Transport protocol (e.g., 'udp' or 'tcp')
            port (`int`): Port number for logging
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []

    if transport_protocol:
        cmd.append(f"logging host ipv6 {host_ip} transport {transport_protocol} port {port}")
    else:
        cmd.append("no logging count")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure IPv6 logging with transport and facility on {device}. Error:\n{e}"
        )
def configure_ipv6_pim_on_interface(device, interface):
    """ Configure ipv6 pim on an interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}",
        "ipv6 pim",
        "end"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 pim on interface {interface}. Error:\n{e}"
        )

def configure_ipv6_logging_with_discriminator(device, syslog_host, discriminator_name, transport_name=None):
    """ Configure IPv6 logging with discriminator on the device
        Args:
            device (`obj`): Device object
            syslog_host (`str`): IPv6 address of the syslog host
            discriminator_name (`str`): Logging discriminator name
            transport_name (`str`, optional): Transport name. Default is None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []

    if discriminator_name:
        if syslog_host:
            cmd.append(f"logging host ipv6 {syslog_host} discriminator {discriminator_name}")
        else:
            cmd.append(f"logging discriminator {discriminator_name}")

    if transport_name:
        cmd.append(f"logging host ipv6 {syslog_host} discriminator {discriminator_name} transport {transport_name}")

    # Add logging count as a separate command
    cmd.append("logging count")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure IPv6 logging with discriminator on {device}. Error:\n{e}"
        )
def configure_logging_host_ipv6(device, ihost_ip, option=None):
    """ Configure logging host IPv6 with a single optional argument
        Args:
            device (`obj`): Device object
            ihost_ip (`str`): IPv6 address of the logging host
            option (`str`, optional): Single option to configure after the IPv6 address.
                                      Valid values: "xml", "sequence-num-session". Default is None.
        Returns:
            None
        Raises:
            SubCommandFailure: If the configuration fails.
    """
    # Build the command
    if option:
        cmd = [f"logging host ipv6 {ihost_ip} {option}"]
    else:
        cmd = [f"logging host ipv6 {ihost_ip}"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure logging host IPv6 with command '{cmd}'. Error:\n{e}"
        )


def unconfigure_logging_host_ipv6(device, syslog_host=None, transport_name=None, host_ip=None):
    """ Unconfigure logging host IPv6
        Args:
            device (`obj`): Device object
            syslog_host (`str`, optional): Syslog host IPv6 address. Default is None.
            transport_name (`str`, optional): Transport protocol name. Default is None.
            host_ip (`str`, optional): IPv6 address of the host. Default is None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []

    if syslog_host and transport_name:
        cmd.append(f'no logging host ipv6 {syslog_host} transport {transport_name}')
    elif host_ip and transport_name:
        cmd.append(f'no logging host ipv6 {host_ip} transport udp port 123')
    elif host_ip:
        cmd.append(f'no logging host ipv6 {host_ip}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure logging host IPv6 with command(s): {cmd}. Error:\n{e}"
        )
        
        
def unconfigure_ipv6_flow_monitor_sampler(device, interface, direction, monitor_name, sampler_name):
    """ UnConfigure IPv6 flow monitor sampler on the specified interface.
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            direction (`str`): Direction of monitor (input/output/both)
            monitor_name (`str`): The flow monitor name
            sampler_name (`str`): The sampler name
        Returns:
            None
        Raises:
            SubCommandFailure:
    """
    cmd = [
        f"interface {interface}",  
        f"no ipv6 flow monitor {monitor_name} sampler {sampler_name} {direction}",
        "end"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure IPv6 flow monitor sampler on {interface}. Error: {e}")
        raise SubCommandFailure(
            f"Could not unconfigure IPv6 flow monitor sampler on {device} for {interface}. Error:\n{e}"
        )

def unconfigure_logging_facility_and_trap(device):
    """ Unconfigure logging facility and trap debugging
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "no logging facility local0",
        "no logging trap debugging"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure logging facility and trap debugging on {device}. Error:\n{e}"
        )


def configure_ipv6_nd_reachable_time(device, reachable_time):
    """ Configure ipv6 nd reachable-time
        Args:
            device (`obj`): Device object
            reachable_time ('int') : Reachability time in milliseconds
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'ipv6 nd reachable-time {reachable_time}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ipv6 nd reachable-time on {device}. Error:\n{e}")


def unconfigure_ipv6_nd_reachable_time(device):
    """ Unconfigure ipv6 nd reachable-time
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure('no ipv6 nd reachable-time')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ipv6 nd reachable-time on {device}. Error:\n{e}")
