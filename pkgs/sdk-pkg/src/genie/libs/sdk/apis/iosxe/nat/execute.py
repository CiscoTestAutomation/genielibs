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