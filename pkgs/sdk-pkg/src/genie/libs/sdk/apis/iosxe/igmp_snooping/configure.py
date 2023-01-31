"""Common configure functions for IGMP snooping"""

import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ip_igmp_snooping_querier(device):
    """Configure IGMP snooping querier 
    
    Args:
        device('obj'): Device object
            
    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    """
    try:
        device.configure("ip igmp snooping querier")

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp snooping querier")

def unconfigure_ip_igmp_snooping_querier(device):
    """
    Unconfigure IGMP snooping querier configuration globally

    Args:
        device('obj'): Device object
            
    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    """
    
    try:
        device.configure("no ip igmp snooping querier")

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ip igmp snooping querier")

    

def configure_ip_igmp_snooping_vlan_querier(device, vlan_id, querier_ip):
    """Configure IGMP snooping vlanquerier configuration
    Example : ip igmp snooping vlan 200 querier address 12.1.1.1

    Args:
        device('obj'): Device object
        vlan_id('int'): vlan id of the switch
        querier_ip('str'): querier IP address
            
    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    """
    try:
        device.configure("ip igmp snooping vlan {} querier address {}".format(vlan_id, querier_ip))

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp snooping vlan id querier address")



def unconfigure_ip_igmp_snooping_vlan_querier(device, vlan_id, querier_ip):
    """UnConfigure IGMP snooping vlan querier configuration
        Example : ip igmp snooping vlan 200 querier address 12.1.1.1

    Args:
        device('obj'): Device object
        vlan_id('int'): vlan id of the switch
        querier_ip('str'): querier IP address
            
    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    """
    try:
        device.configure("no ip igmp snooping vlan {} querier address {}".format(vlan_id, querier_ip))

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ip igmp snooping vlan id querier address") 


def configure_ip_igmp_snooping_vlan_query_version(device, vlan_id, version_num):
            
    """Configure IGMP snooping vlan querier version configuration
        Example : ip igmp snooping vlan 200 querier version 3

    Args:
        device('obj'): Device object
        vlan_id('int'): vlan id of the switch
        version_num('int'): IP IGMP version number

    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    """

    try:
        device.configure("ip igmp snooping vlan {} querier version {}".format(vlan_id, version_num))

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp snooping vlan query version")      


def unconfigure_ip_igmp_snooping_vlan_query_version(device, vlan_id, version_num):
    """UnConfigure IGMP snooping vlan querier configuration
        Example : no ip igmp snooping vlan 200 querier version 3

    Args:
        device('obj'): Device object
        vlan_id('int'): vlan id of the switch
        version_num('int'): IP IGMP version number of the switch
            
    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    """
    try:
        device.configure("no ip igmp snooping vlan {} querier version {}".format(vlan_id, version_num))

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp snooping vlan query version") 

def configure_ip_igmp_snooping(device):
    """UnConfigure IGMP snooping 
        Example : ip igmp snooping 

    Args:
        device('obj'): Device object
            
    Returns:
        None
    
    Raises:
        SubCommandFailure : Could not configure ip igmp snooping
    
    """
    config = "ip igmp snooping"
    try:
        device.configure(config)

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp snooping") 

def unconfigure_ip_igmp_snooping(device):
    """UnConfigure IGMP snooping 
        Example : no ip igmp snooping 

    Args:
        device('obj'): Device object
            
    Returns:
        None
    
    Raises:
        SubCommandFailure : Could not unconfigure ip igmp snooping
    
    """
    config = "no ip igmp snooping"
    try:
        device.configure(config)

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ip igmp snooping") 



def configure_ip_igmp_snooping_vlan_vlanid(device, vlan_id):
            
    """Configure IGMP snooping vlan configuration
        Example : ip igmp snooping vlan 200
    Args:
        device('obj'): Device object
        vlan_id('int'): vlan id of the switch
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = "ip igmp snooping vlan {}".format(vlan_id)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip igmp snooping vlan query version Error:\n{error}".format(
                error=e,
            )
        )

def unconfigure_ip_igmp_snooping_vlan_vlanid(device, vlan_id):
    """UnConfigure IGMP snooping vlan configuration
        Example : no ip igmp snooping vlan 200 
    Args:
        device('obj'): Device object
        vlan_id('int'): vlan id of the switch            
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = "no ip igmp snooping vlan {}".format(vlan_id)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip igmp snooping vlan Error:\n{error}".format(
                error=e,
            )
        )


def configure_igmp_snooping_tcn_flood(device, interface):
    """Configure IGMP snooping tcn flooding
    Args:
        device('obj'): Device object
        interface('str'): interface in which tcn flooding needs to be enabled
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    configs = []
    configs.append("interface {interface}".format(interface=interface))
    configs.append("ip igmp snooping tcn flood")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp snooping tcn flood on {device.name}. Error:\n{e}")
def unconfigure_igmp_snooping_tcn_flood(device, interface):
    """unconfigure IGMP snooping tcn flooding
    Args:
        device('obj'): Device object
        interface('str'): interface in which tcn flooding needs to be disabled
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    configs = []
    configs.append("interface {interface}".format(interface=interface))
    configs.append("no ip igmp snooping tcn flood")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ip igmp snooping tcn flood on {device.name}. Error:\n{e}")

def configure_ip_igmp_snooping_vlan_static(device, vlan_id, group_ip, interface):
    """
    Configure IGMP snooping vlan static configuration
    Example : ip igmp snooping vlan 200 static 225.0.0.100 interface gig 1/0/1

    Args:
        device('obj'): Device object
        vlan_id('int'): vlan id of the switch
        group_ip('str'): group ip address
        interface('str'): interface name

    Returns:
        None

    Raises:
        SubCommandFailure
    """
    cmd = f"ip igmp snooping vlan {vlan_id} static {group_ip} interface {interface}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not configure ip igmp snooping vlan id static interface. Error:\n{e}")

def unconfigure_ip_igmp_snooping_vlan_static(device, vlan_id, group_ip, interface):
    """
    Unconfigure IGMP snooping vlan static configuration
    Example : no ip igmp snooping vlan 200 static 225.0.0.100 interface gig 1/0/1

    Args:
        device('obj'): Device object
        vlan_id('int'): vlan id of the switch
        group_ip('str'): group ip address
        interface('str'): interface name

    Returns:
        None

    Raises:
        SubCommandFailure
    """
    cmd = f"no ip igmp snooping vlan {vlan_id} static {group_ip} interface {interface}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not unconfigure ip igmp snooping vlan id static interface. Error:\n{e}")

