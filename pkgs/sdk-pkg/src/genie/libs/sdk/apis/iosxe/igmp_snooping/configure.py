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

def configure_ip_igmp_querier_query_interval(device, query_type, query_interval):
    """
    Configure ip igmp snooping querier query-interval 100

    Args:
        device('obj'): Device object
        query_type('str'): query-interval     IGMP querier query interval (sec)
        query_interval('int'): <1-18000>  IGMP querier query interval (sec)
        
    Returns:
        None

    Raises:
        SubCommandFailure
    """
    cmd = f"ip igmp snooping querier {query_type} {query_interval}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not configure ip igmp snooping querier query-interval. Error:\n{e}")

def configure_ip_igmp_querier_tcn_query_count(device, query_type, action_type, query_count):
    """
    Configure ip igmp snooping querier tcn query count 10

    Args:
        device('obj'): Device object
        query_type('str'):tcn                IGMP querier TCN related parameters
        action_type('str'): count     IGMP querier TCN query count
                            interval  IGMP querier TCN query interval (sec)
        query_count('int'):<1-10>  IGMP querier TCN query count
        
    Returns:
        None

    Raises:
        SubCommandFailure
    """
    cmd = f"ip igmp snooping querier {query_type} query {action_type} {query_count}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not configure ip igmp snooping querier tcn query count 10. Error:\n{e}")
  
def unconfigure_ip_igmp_querier_query_interval(device, query_type, query_interval):
    """
    Unconfigure ip igmp snooping querier query-interval 100

    Args:
        device('obj'): Device object
        query_type('str'): query-interval     IGMP querier query interval (sec)
        query_interval('int'): <1-18000>  IGMP querier query interval (sec)
        
    Returns:
        None

    Raises:
        SubCommandFailure
    """
    cmd = f"no ip igmp snooping querier {query_type} {query_interval}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not unconfigure ip igmp snooping querier query-interval. Error:\n{e}")
    
def unconfigure_ip_igmp_querier_max_response_time(device, query_type, query_time):
    """
    Unconfigure ip igmp snooping querier max response time 25

    Args:
        device('obj'): Device object
        query_type('str'): max-response-time     IGMP querier max response time (sec)
        query_time('int'): <1-500>  IGMP querier query response time (sec)
        
    Returns:
        None

    Raises:
        SubCommandFailure
    """
    cmd = f"no ip igmp snooping querier {query_type} {query_time}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not unconfigure ip igmp snooping querier max response time 25. Error:\n{e}")

def unconfigure_ip_igmp_querier_tcn_query_count(device, query_type, action_type, query_count):
    """
    Unconfigure ip igmp snooping querier tcn query count 10
    Args:
        device('obj'): Device object
        query_type('str'):tcn                IGMP querier TCN related parameters
        action_type('str'): count     IGMP querier TCN query count
        query_count('int'):<1-10>  IGMP querier TCN query count
        
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"no ip igmp snooping querier {query_type} query {action_type} {query_count}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not unconfigure ip igmp snooping querier tcn query count 10. Error:\n{e}")
    
def unconfigure_ip_igmp_querier_tcn_query_interval(device, query_type, action_type, query_interval):
    """
    Unconfigure ip igmp snooping querier tcn query interval 255
    Args:
        device('obj'): Device object
        query_type('str'):tcn              IGMP querier TCN related parameters
        action_type('str'): interval       IGMP querier TCN query interval
        query_interval('int'):<1-500>      IGMP querier TCN query count (sec)
        
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"no ip igmp snooping querier {query_type} query {action_type} {query_interval}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not unconfigure ip igmp snooping querier tcn query count 10. Error:\n{e}")
    
def unconfigure_ip_igmp_querier_timer_expiry(device, query_time):
    """
    Unconfigure ip igmp snooping querier timer expiry 300
    Args:
        device('obj'): Device object
        query_time('int'):<1-500>  IGMP querier timer expiry count (sec)
        
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"no ip igmp snooping querier timer expiry {query_time}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not unconfigure ip igmp snooping querier timer expiry 300. Error:\n{e}")
        
def configure_ip_igmp_filter(device):
    """Configure IGMP filter     
    Args:
        device('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    
    """
    try:
        out = device.configure("ip igmp filter")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp filter")
    return out
        
def unconfigure_ip_igmp_filter(device):
    """UnConfigure IGMP filter     
    Args:
        device('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    
    """
    try:
        out = device.configure("no ip igmp filter")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ip igmp filter")
    return out
        
def configure_igmp_filter_on_interface(device, interface, filter_profile_number):
    """Configure IGMP filter on interface
    Args:
        device('obj'): Device object
        interface('str'): interface on which filter has to be configured
        filter_profile_number('str'):  IGMP profile number
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    configs = []
    configs.append(f"interface {interface}")
    configs.append(f"ip igmp filter {filter_profile_number}")
   
    try:
        out = device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp filter on interface. Error:\n{e}")
    return out
        
def unconfigure_igmp_filter_on_interface(device, interface, filter_profile_number):
    """UnConfigure IGMP filter on interface
    Args:
        device('obj'): Device object
        interface('str'): interface on which filter has to be configured
        filter_profile_number('str'):  IGMP profile number
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    configs = []
    configs.append(f"interface {interface}")
    configs.append(f"no ip igmp filter {filter_profile_number}")
   
    try:
        out = device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ip igmp filter on interface. Error:\n{e}")
    return out
        
def configure_igmp_profile(device, profile_id, permission=None, range_address=None):
    """Configure IGMP profile
    Args:
        device('obj'): Device object
        profile_id('str'): Profile number
        permission('str'):  permit or deny
        range_address('str'):  Low IP multicast address
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    configs = []
    configs.append(f"ip igmp profile {profile_id}")
    if permission:
        configs.append(f"{permission}")
    if range_address:
        configs.append(f"range {range_address}")
   
    try:
        out = device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure ip igmp profile. Error:\n{e}")
    return out
        
def unconfigure_igmp_profile(device, profile_id):
    """UnConfigure IGMP profile
    Args:
        device('obj'): Device object
        profile_id('str'): Profile number
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    configs = []
    configs.append(f"no ip igmp profile {profile_id}")
   
    try:
        out = device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure ip igmp profile. Error:\n{e}")
    return out


def configure_ip_igmp_snooping_robustness(device, robustness, vlan=None):
    """
    Configure ip igmp snooping robustness variable
    Args:
        device (`obj`): Device object
        robustness ('int'): IGMP snooping robustness value
        vlan ('int', optional): VLAN ID to apply the robustness value to
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"ip igmp snooping vlan {vlan} robustness-variable {robustness}"
    else:
        cmd = f"ip igmp snooping robustness-variable {robustness}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure IGMP snooping robustness. Error:\n{e}")


def unconfigure_ip_igmp_snooping_robustness(device, vlan=None):
    """
    Unconfigure ip igmp snooping robustness variable
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID to apply the robustness value to
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} robustness-variable"
    else:
        cmd = "no ip igmp snooping robustness-variable"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure IGMP snooping robustness. Error:\n{e}")


def configure_ip_igmp_snooping_check_rtr_alert_option(device, vlan=None):
    """
    Configure ip igmp snooping check router alert option
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID to apply the option to
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"ip igmp snooping vlan {vlan} check rtr-alert-option"
    else:
        cmd = "ip igmp snooping check rtr-alert-option"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure IGMP snooping check router alert "
            f"option. Error:\n{e}")


def unconfigure_ip_igmp_snooping_check_rtr_alert_option(device, vlan=None):
    """
    Unconfigure ip igmp snooping check router alert option
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID to apply the option to
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} check rtr-alert-option"
    else:
        cmd = "no ip igmp snooping check rtr-alert-option"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure IGMP snooping check router alert "
            f"option. Error:\n{e}")


def configure_ip_igmp_snooping_check_ttl(device, vlan=None):
    """
    Configure ip igmp snooping check ttl=1
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID to apply the option to
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"ip igmp snooping vlan {vlan} check ttl"
    else:
        cmd = "ip igmp snooping check ttl"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure IGMP snooping check ttl. Error:\n{e}")


def unconfigure_ip_igmp_snooping_check_ttl(device, vlan=None):
    """
    Unconfigure ip igmp snooping check ttl=1
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID to apply the option to
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} check ttl"
    else:
        cmd = "no ip igmp snooping check ttl"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure IGMP snooping check ttl. Error:\n{e}")


def configure_ip_igmp_snooping_last_member_query_count(
        device, count, vlan=None):
    """
    Configure ip igmp snooping last member query count
    Args:
        device (`obj`): Device object
        count ('int'): IGMP snooping last member query count
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"ip igmp snooping vlan {vlan} last-member-query-count {count}"
    else:
        cmd = f"ip igmp snooping last-member-query-count {count}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure IGMP snooping last member query "
            f"count. Error:\n{e}")


def unconfigure_ip_igmp_snooping_last_member_query_count(device, vlan=None):
    """
    Unconfigure ip igmp snooping last member query count
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} last-member-query-count"
    else:
        cmd = "no ip igmp snooping last-member-query-count"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure IGMP snooping last member query "
            f"count. Error:\n{e}")


def configure_ip_igmp_snooping_last_member_query_interval(
        device, time, vlan=None):
    """
    Configure ip igmp snooping last member query interval
    Args:
        device (`obj`): Device object
        time ('int'): IGMP snooping last member query interval in
                      milliseconds
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = (f"ip igmp snooping vlan {vlan} "
               f"last-member-query-interval {time}")
    else:
        cmd = f"ip igmp snooping last-member-query-interval {time}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure IGMP snooping last member query "
            f"interval. Error:\n{e}")


def unconfigure_ip_igmp_snooping_last_member_query_interval(
        device, vlan=None):
    """
    Unconfigure ip igmp snooping last member query interval
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} last-member-query-interval"
    else:
        cmd = "no ip igmp snooping last-member-query-interval"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure IGMP snooping last member query "
            f"interval. Error:\n{e}")


def configure_ip_igmp_snooping_querier_address(device, address, vlan=None):
    """
    Configure ip igmp snooping querier address
    Args:
        device (`obj`): Device object
        address ('str'): IGMP snooping querier address
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"ip igmp snooping vlan {vlan} querier address {address}"
    else:
        cmd = f"ip igmp snooping querier address {address}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure IGMP snooping querier address. "
            f"Error:\n{e}")


def unconfigure_ip_igmp_snooping_querier_address(device, vlan=None):
    """
    Unconfigure ip igmp snooping querier address
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} querier address"
    else:
        cmd = "no ip igmp snooping querier address"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure IGMP snooping querier address. "
            f"Error:\n{e}")


def configure_ip_igmp_snooping_querier_interval(device, interval, vlan=None):
    """
    Configure ip igmp snooping querier interval
    Args:
        device (`obj`): Device object
        interval ('int'): IGMP snooping querier interval in seconds
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = (f"ip igmp snooping vlan {vlan} "
               f"querier query-interval {interval}")
    else:
        cmd = f"ip igmp snooping querier query-interval {interval}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure IGMP snooping querier interval. "
            f"Error:\n{e}")


def unconfigure_ip_igmp_snooping_querier_interval(device, vlan=None):
    """
    Unconfigure ip igmp snooping querier interval
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} querier query-interval"
    else:
        cmd = "no ip igmp snooping querier query-interval"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure IGMP snooping querier interval. "
            f"Error:\n{e}")


def configure_ip_igmp_snooping_querier_max_response_time(
        device, max_response_time, vlan=None):
    """
    Configure ip igmp snooping querier max response time
    Args:
        device (`obj`): Device object
        max_response_time ('int'): IGMP snooping querier max response time
                                   in seconds
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = (f"ip igmp snooping vlan {vlan} querier "
               f"max-response-time {max_response_time}")
    else:
        cmd = (f"ip igmp snooping querier "
               f"max-response-time {max_response_time}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure IGMP snooping querier max response "
            f"time. Error:\n{e}")


def unconfigure_ip_igmp_snooping_querier_max_response_time(
        device, vlan=None):
    """
    Unconfigure ip igmp snooping querier max response time
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} querier max-response-time"
    else:
        cmd = "no ip igmp snooping querier max-response-time"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure IGMP snooping querier max response "
            f"time. Error:\n{e}")


def configure_ip_igmp_snooping_querier_version(device, version, vlan=None):
    """
    Configure ip igmp snooping querier version
    Args:
        device (`obj`): Device object
        version ('int'): IGMP snooping querier version
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"ip igmp snooping vlan {vlan} querier version {version}"
    else:
        cmd = f"ip igmp snooping querier version {version}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure IGMP snooping querier version. "
            f"Error:\n{e}")


def unconfigure_ip_igmp_snooping_querier_version(device, vlan=None):
    """
    Unconfigure ip igmp snooping querier version
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} querier version"
    else:
        cmd = "no ip igmp snooping querier version"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure IGMP snooping querier version. "
            f"Error:\n{e}")


def configure_ip_igmp_snooping_immediate_leave(device, vlan=None):
    """
    Configure ip igmp snooping immediate leave
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"ip igmp snooping vlan {vlan} immediate-leave"
    else:
        cmd = "ip igmp snooping immediate-leave"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure IGMP snooping immediate leave. "
            f"Error:\n{e}")


def unconfigure_ip_igmp_snooping_immediate_leave(device, vlan=None):
    """
    Unconfigure ip igmp snooping immediate leave
    Args:
        device (`obj`): Device object
        vlan ('int', optional): VLAN ID
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vlan:
        cmd = f"no ip igmp snooping vlan {vlan} immediate-leave"
    else:
        cmd = "no ip igmp snooping immediate-leave"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure IGMP snooping immediate leave. "
            f"Error:\n{e}")
