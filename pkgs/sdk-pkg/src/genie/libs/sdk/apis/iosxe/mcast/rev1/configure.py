"""Unified implementations for ip multicast routing configuration (rev1)"""

# Python
import logging
import warnings

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_pim_autorp_listener(device, vrf=None, intf=None, loopback_number=None, ttl=None, announce=True, discovery=True):
    
    """ Config pim autorp listener
        Args:
            device ('obj'): Device object
            vrf ('str', optional): Name of the vrf (for VRF context)
            intf ('str', optional): Name of the interface (for VRF context)
            loopback_number ('int', optional): Loopback number (for global context)
            ttl ('int'): TTL value
            announce ('bool'): True or False
            discovery ('bool'): True or False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
  
    '''
    VRF context:
        ip pim vrf <vrf> autorp listener
        ip pim vrf <vrf> send-rp-discovery scope <ttl>
        ip pim vrf <vrf> send-rp-announce <intf> scope <ttl>
    Global context:
        ip pim autorp listener
        ip pim send-rp-discovery loopback <loopback_number> scope <ttl>
        ip pim send-rp-announce loopback <loopback_number> scope <ttl>
    '''
    
    configs = []
    
    if vrf:
        # VRF context
        configs.append(f"ip pim vrf {vrf} autorp listener")
        
        if discovery and ttl:
            configs.append(f"ip pim vrf {vrf} send-rp-discovery scope {ttl}")
                           
        if announce and intf and ttl:
            configs.append(f"ip pim vrf {vrf} send-rp-announce {intf} scope {ttl}")
    else:
        # Global context
        configs.append(f"ip pim autorp listener")
        
        if discovery and loopback_number and ttl:
            configs.append(f"ip pim send-rp-discovery loopback {loopback_number} scope {ttl}")
                           
        if announce and loopback_number and ttl:
            configs.append(f"ip pim send-rp-announce loopback {loopback_number} scope {ttl}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure pim autorp listener. Error:{e}")


def unconfigure_pim_autorp_listener(device, vrf=None, intf=None, loopback_number=None, ttl=None, announce=True, discovery=True):
    
    """ Unconfig pim autorp listener
        Args:
            device ('obj'): Device object
            vrf ('str', optional): Name of the vrf (for VRF context)
            intf ('str', optional): Name of the interface (for VRF context)
            loopback_number ('int', optional): Loopback number (for global context)
            ttl ('int'): TTL value
            announce ('bool'): True or False
            discovery ('bool'): True or False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
  
    '''
    VRF context:
        no ip pim vrf <vrf> autorp listener
        no ip pim vrf <vrf> send-rp-discovery scope <ttl>
        no ip pim vrf <vrf> send-rp-announce <intf> scope <ttl>
    Global context:
        no ip pim autorp listener
        no ip pim send-rp-discovery loopback <loopback_number> scope <ttl>
        no ip pim send-rp-announce loopback <loopback_number> scope <ttl>
    '''
    
    configs = []
    
    if vrf:
        # VRF context
        configs.append(f"no ip pim vrf {vrf} autorp listener")
        
        if discovery and ttl:
            configs.append(f"no ip pim vrf {vrf} send-rp-discovery scope {ttl}")
                           
        if announce and intf and ttl:
            configs.append(f"no ip pim vrf {vrf} send-rp-announce {intf} scope {ttl}")
    else:
        # Global context
        configs.append(f"no ip pim autorp listener")
        
        if discovery and loopback_number and ttl:
            configs.append(f"no ip pim send-rp-discovery loopback {loopback_number} scope {ttl}")
                           
        if announce and loopback_number and ttl:
            configs.append(f"no ip pim send-rp-announce loopback {loopback_number} scope {ttl}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure pim autorp listener. Error:{e}")