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
        version_num('int'): IP IGMP version number
            
    Returns:
        None
    
    Raises:
        SubCommandFailure
    
    """
    try:
        device.configure("no ip igmp snooping vlan {} querier address {}".format(vlan_id, version_num))

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp snooping vlan query version") 
