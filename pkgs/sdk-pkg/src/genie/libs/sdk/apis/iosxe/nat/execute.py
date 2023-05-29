import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

"""Execute CLI functions for nat"""
def execute_clear_nat_translation(device):
    """ Clear All NAT Flows

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = "clear ip nat translation *"
    
    try:
        out = device.execute(cmd)
    except Exception  as err:
        raise Exception(err)

    return out
    
def execute_clear_nat64_statistics(device):
    """ clear nat64 statistics
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear nat64 statistics")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear nat64 statistics on device")
        
def execute_clear_nat64_statistics_failure(device):
    """ clear nat64 statistics failure
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear nat64 statistics failure")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear nat64 statistics failure on device")
        
def execute_clear_nat64_statistics_global(device):
    """ clear nat64 statistics global
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear nat64 statistics global")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear nat64 statistics global on device")
        
def execute_clear_nat64_statistics_interface(device, interface_name):
    """ clear nat64 statistics interface {interface_name}
        Args:
            device ('obj'): Device object
            interface_name('str'): Interface name to clear nat64 statistics interface {interface_name}
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"clear nat64 statistics interface {interface_name}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear nat64 statistics interface {interface_name} on device")
        
def execute_clear_nat64_statistics_pool(device, pool_name):
    """ clear nat64 statistics pool {pool_name}
        Args:
            device ('obj'): Device object
            pool_name('str'): Pool name to clear nat64 statistics
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"clear nat64 statistics pool {pool_name}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear nat64 statistics pool {pool_name} on device")
        
def execute_clear_nat64_statistics_prefix_stateful(device, ipv6_address, prefix_length):
    """ clear nat64 statistics prefix stateful {ipv6_address}/{prefix_length}
        Args:
            device ('obj'): Device object
            ipv6_address('str'): IPv6 Address to clear nat64 statistics prefix stateful {ipv6_address}/{prefix_length}
            prefix_length('str'): Prefix length to clear nat64 statistics prefix stateful {ipv6_address}/{prefix_length}
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"clear nat64 statistics prefix stateful {ipv6_address}/{prefix_length}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear nat64 statistics prefix stateful {ipv6_address}/{prefix_length} on device")
        
def execute_clear_nat64_translations_all(device):
    """ clear nat64 translations all
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear nat64 translations all")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear nat64 translations all")
        
def execute_clear_nat64_translations_protocol(device, protocol_name):
    """ clear nat64 translations protocol {protocol_name}
        Args:
            device ('obj'): Device object
            protocol_name('str'): Protocl name to clear nat64 translations protocol {protocol_name}
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"clear nat64 translations protocol {protocol_name}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear nat64 translations protocol {protocol_name} on device")


def execute_clear_ip_nat_translation(device, tcp=False, udp=False, forced=False, inside_local_ip=None, 
    inside_global_ip=None, inside_local_port=None, inside_global_port=None, outside_local_ip=None, 
    outside_global_ip=None, outside_local_port=None, outside_global_port=None):
    """ Clear IP NAT Flows
        Args:
            device ('obj'): Device object
            tcp ('bool', optional): clear ip nat tcp. Default to False.
            udp ('bool', optional): clear ip nat udp. Default to False.
            forced ('bool', optional): clear ip nat forcefully. Default to False.
            inside_local_ip ('str', optional): Inside local ip address. Default to None.
            inside_global_ip ('str', optional): Inside global ip address. Default to None.
            inside_local_port ('str', optional): Inside local port in case of tcp/udp. Default to None.
            inside_global_port ('str', optional): Inside global port in case of tcp/udp. Default to None.
            outside_local_ip ('str', optional): Outside local ip address. Default to None.
            outside_global_ip ('str', optional): Outside global ip address. Default to None.
            outside_local_port ('str', optional): Outside local port in case of tcp/udp. Default to None.
            outside_global_port ('str', optional): Outside global port in case of tcp/udp. Default to None.

        Returns:
            output

        Raises:
            SubCommandFailure
    """
    cmd = 'clear ip nat translation'

    if tcp:
        cmd += ' tcp'
    elif udp:
        cmd += ' udp'
    if inside_global_ip and inside_local_ip:
        cmd += f' inside {inside_global_ip}{f" {inside_global_port}" if inside_global_port else ""} {inside_local_ip}{f" {inside_local_port}" if inside_local_port else ""}'
    if outside_local_ip and outside_global_ip:
        cmd += f' outside {outside_local_ip}{f" {outside_local_port}" if outside_local_port else ""} {outside_global_ip}{f" {outside_global_port}" if outside_global_port else ""}'
    if forced:
        cmd += ' forced'
    
    try:
        out = device.execute(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear ip nat translation. Error:{e}")

    return out
