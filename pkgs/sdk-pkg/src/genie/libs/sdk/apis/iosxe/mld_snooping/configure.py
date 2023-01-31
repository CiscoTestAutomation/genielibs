"""Common configure functions for MLD snooping"""

import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ipv6_mld_snooping(device):
    """Configure IPv6 MLD Snooping 
      
    Args:
        device('obj'): Device object
    
    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("ipv6 mld snooping")
        
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("could not configure ipv6 mld snooping")   

def unconfigure_ipv6_mld_snooping(device):
    """Unconfigure IPv6 MLD Snooping on the switch
      
    Args:
        device('obj'): Device object
    
    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("no ipv6 mld snooping")
        
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("could not unconfigure ipv6 mld snooping")   


def configure_ipv6_mld_snooping_querier_version(device, version_num):

    """Configure IPv6 MLD Snooping Querier version number
      
    Args:
        device('obj'): Device object
        version_num('int'): ipv6 mld snooping querier version number
    
    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("ipv6 mld snooping querier version {}".format(version_num))
    
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ipv6 mld snooping querier version in the device")


def unconfigure_ipv6_mld_snooping_querier_version(device, version_num):

    """Unconfigure IPv6 MLD Snooping Querier version number
      
    Args:
        device('obj'): Device object
        version_num('int'): ipv6 mld snooping querier version number
    
    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("no ipv6 mld snooping querier version {}".format(version_num))
    
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ipv6 mld snooping querier version in the device")


def configure_ipv6_mld_snooping_querier_address(device, ipv6_address):

    """Configure IPv6 MLD Snooping Querier address
       Example : ipv6 mld snooping querier address ipv6_address
      
    Args:
        device('obj'): Device object
        ipv6_address('str'): IPv6 address of the MLD source address which needs to be Link-Local range

    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("ipv6 mld snooping querier address {}".format(ipv6_address))
    
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ipv6 mld snooping querier address in the device")


def unconfigure_ipv6_mld_snooping_querier_address(device, ipv6_address):

    """Unconfigure IPv6 MLD Snooping Querier address
       Example : ipv6 mld snooping querier address ipv6_address
      
    Args:
        device('obj'): Device object
        ipv6_address('str'): IPv6 address of the MLD source address which needs to be Link-Local range

    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("no ipv6 mld snooping querier address {}".format(ipv6_address))
    
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ipv6 mld snooping querier address in the device")


def configure_ipv6_mld_snooping_vlan_querier_version(device, vlan_id, version_num):

    """Configure IPv6 MLD Snooping VLAN Querier version
       Example : ipv6 mld snooping vlan 200 querier version 2
      
    Args:
        device('obj'): Device object
        vlan_id('int'): VLAN ID of the device
        version_num('int'): MLD Snooping version of the device

    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("ipv6 mld snooping vlan {} querier version {}".format(vlan_id, version_num))
    
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ipv6 mld snooping vlan querier version on the device")


def unconfigure_ipv6_mld_snooping_vlan_querier_version(device, vlan_id, version_num):

    """Unconfigure IPv6 MLD Snooping VLAN Querier version 
       Example : no ipv6 mld snooping vlan 200 querier version 2
      
    Args:
        device('obj'): Device object
        vlan_id('int'): VLAN ID of the device
        version_num('int'): MLD Snooping version of the device

    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("no ipv6 mld snooping vlan {} querier version {}".format(vlan_id, version_num))
    
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ipv6 mld snooping vlan querier address in the device")

def configure_ipv6_mld_snooping_querier(device):

    """Configure ipv6 mld snooping querier 
       Example : ipv6 mld snooping querier 
      
    Args:
        device('obj'): Device object
       
    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("ipv6 mld snooping querier")
    
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ipv6 mld snooping querier in the device")


def unconfigure_ipv6_mld_snooping_querier(device):

    """Unconfigure ipv6 mld snooping querier
       Example : ipv6 mld snooping querier
      
    Args:
        device('obj'): Device object


    Returns:
        None
    
    Raises: 
        SubCommandFailure
    """
    try:
        device.configure("no ipv6 mld snooping querier")
    
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ipv6 mld snooping querier in the device")
def configure_ipv6_mld_snooping_tcn_flood(device, interface):
    """Configure IPv6 MLD snooping tcn flooding
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
    configs.append("ipv6 mld snooping tcn flood")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ipv6 mld snooping tcn flood on {device.name}. Error:\n{e}")
def unconfigure_ipv6_mld_snooping_tcn_flood(device, interface):
    """unconfigure IPv6 MLD snooping tcn flooding
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
    configs.append("no ipv6 mld snooping tcn flood")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ipv6 mld snooping tcn flood on {device.name}. Error:\n{e}")
