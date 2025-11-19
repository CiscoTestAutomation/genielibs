"""Common configure/unconfigure functions for DMVPN"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)



def configure_interface_tunnel_hub(device,
                            tunnel_intf,
                            tunnel_ip,
                            tunnel_mask,
                            tunnel_src,
                            vrf_forwarding = None,
                            tunnel_vrf = None,
                            holdtimer = None,
                            tunnel_key_id= None,
                            ipsec_profile_name= None,
                            ip_redirects= False,
                            authentication_string= None,
                            network_id = None,
                            gre_multipoint = False,
                            ipsec = False,
                            dual_overlay = False,
                            type= '',
                            ipv6_enable= False):
    """ Configures interface Tunnel[number] hub
        Args:
            device ('obj'): Device object
            tunnel_intf ('str'): tunnel interface
            tunnel_ip ('str'): tunnel ip address
            tunnel_mask ('str'): tunnel mask
            tunnel_src ('str'): tunnel source 
            ipsec_profile_name ('str',optional): IPSEC profile name
            authentication_string ('str',optional): Authentication string 
            network_id ('int',optional): Network Identifier
            holdtimer ('int',optional): Number of seconds with respect to HoldTimer
            tunnel_key_id ('int',optional) : Tunnel key used 
            ip_redirects ('boolean',optional): Setting ip redirects.Defaults to False.
            gre_multipoint ('boolean',optional) : Setting gre_multipoint in case "gre multipoint" option is chosen.Defaults to False.
            ipsec ('boolean',optional) : Setting ipsec in case "ipsec" option is chosen.Defaults to False.
            dual_overlay ('boolean',optional) : Setting dual_overlay for tunnel mode 
            ipsec dual-overlay option.Defaults to False.
            type ('str',optional) : Type of IP address [Ipv4 or Ipv6]
            ipv6_enable ('boolean',optional) : Setting ipv6 enable.Defaults to False.
            vrf_forwarding ('str',optional) : Configured VRF name to be entered.
            tunnel_vrf ('str',optional): Configured VRF table name to be entered.

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring interface tunnel[number] hub"
    )

    configs = []
    configs.append("interface {tunnel_intf}".format(tunnel_intf=tunnel_intf))

    if vrf_forwarding is not None:    
        configs.append("vrf forwarding {vrf_forwarding}".format(vrf_forwarding=vrf_forwarding))

    if tunnel_vrf is not None:    
        configs.append("tunnel vrf {tunnel_vrf}".format(tunnel_vrf=tunnel_vrf))    

    configs.append("ip address {tunnel_ip} {tunnel_mask}".format(tunnel_ip=tunnel_ip,tunnel_mask=tunnel_mask))    
    configs.append("tunnel source {tunnel_src}".format(tunnel_src=tunnel_src))
    configs.append("ip nhrp map multicast dynamic")
    if ipsec_profile_name is not None:
        configs.append("tunnel protection ipsec profile {ipsec_profile_name}".format(ipsec_profile_name=ipsec_profile_name))

    if authentication_string is not None:
        configs.append("ip nhrp authentication {authentication_string}".format(authentication_string=authentication_string))

    if network_id is not None:
        configs.append("ip nhrp network-id {network_id}".format(network_id=network_id))

    if holdtimer is not None:          
        configs.append("ip nhrp holdtime {holdtimer}".format(holdtimer=holdtimer))

    if tunnel_key_id is not None:    
        configs.append("tunnel key {tunnel_key_id}".format(tunnel_key_id=tunnel_key_id))

    if ip_redirects:
        configs.append("no ip redirects")    

    if gre_multipoint:
        configs.append("tunnel mode gre multipoint")
    elif ipsec:
        if dual_overlay is True :
            configs.append("tunnel mode ipsec dual-overlay")
        elif (dual_overlay is False and type == 'ipv4' ):
            configs.append("tunnel mode ipsec ipv4 v6-overlay")
        elif (dual_overlay is False and type == 'ipv6' ):
            configs.append("tunnel mode ipsec ipv6 v4-overlay")       
    
    if ipv6_enable:
        configs.append("ipv6 enable")    

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure interface Tunnel hub,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_interface_tunnel_spoke(device,
                            tunnel_intf,
                            tunnel_ip,
                            tunnel_mask,
                            tunnel_src,
                            vrf_forwarding = None,
                            tunnel_vrf = None,                            
                            ipsec_profile_name= None,                            
                            authentication_string= None,
                            network_id= None,
                            holdtimer= None,
                            tunnel_key_id = None,
                            next_hop_server_ip= None,
                            nbma_ip_address= None,
                            gre_multipoint=False,
                            ipsec= False,
                            type='',
                            dual_overlay=False,
                            tunnel_destination= None,
                            ipv6_enable=False,
                            ip_redirects=False                             
                            ):                            
    """ Configures interface Tunnel spoke
        Args:
            device ('obj'): Device object
            tunnel_intf ('str'): tunnel interface
            tunnel_ip ('str'): tunnel ip address
            tunnel_mask ('str'): tunnel mask
            tunnel_src ('str'): tunnel source 
            ipsec_profile_name ('str',optional): IPSEC profile name
            authentication_string ('str',optional): Authentication string 
            network_id ('int',optional): Network Identifier
            holdtimer ('int',optional): Number of seconds with respect to HoldTimer
            tunnel_key_id ('int',optional) : Tunnel key used
            next_hop_server_ip ('str',optional) : Protocol IP address of NHS
            nbma_ip_address ('str',optional) : NBMA IP address
            ipv6_enable ('boolean',optional) : setting ipv6 enable.Defaults to False.
            tunnel_destination ('str',optional) : Tunnel destination IP address
            gre_multipoint ('boolean',optional) : setting gre_multipoint in case "gre multipoint" option is chosen.Defaults to False.
            ipsec ('boolean',optional) : setting ipsec in case "ipsec" option is  chosen.Defaults to False.
            dual_overlay ('boolean',optional) : setting dual_overlay for tunnel mode ipsec dual-overlay option.Defaults to False.
            type ('str',optional) : Type of IP address [Ipv4 or Ipv6]
            ip_redirects ('boolean',optional): setting ip redirects .Defaults to False.
            vrf_forwarding ('str',optional) : Configured VRF name to be entered.
            tunnel_vrf ('str',optional): Configured VRF table name to be entered.


        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring interface Tunnel[number] spoke"
    )

    configs = []
    configs.append("interface {tunnel_intf}".format(tunnel_intf=tunnel_intf))

    if vrf_forwarding is not None:    
        configs.append("vrf forwarding {vrf_forwarding}".format(vrf_forwarding=vrf_forwarding))

    if tunnel_vrf is not None:    
        configs.append("tunnel vrf {tunnel_vrf}".format(tunnel_vrf=tunnel_vrf))    

    configs.append("ip address {tunnel_ip} {tunnel_mask}".format(tunnel_ip=tunnel_ip,tunnel_mask=tunnel_mask))
    configs.append("tunnel source {tunnel_src}".format(tunnel_src=tunnel_src))  

    if ipsec_profile_name is not None:
        configs.append("tunnel protection ipsec profile {ipsec_profile_name}".format(ipsec_profile_name=ipsec_profile_name))    
    
    if ip_redirects:
        configs.append("no ip redirects")   

    if authentication_string is not None:
        configs.append("ip nhrp authentication {authentication_string}".format(authentication_string=authentication_string))
    
    if network_id is not None:
        configs.append("ip nhrp network-id {network_id}".format(network_id=network_id))      
    
    if holdtimer is not None:
        configs.append("ip nhrp holdtime {holdtimer}".format(holdtimer=holdtimer))
    
    if tunnel_key_id is not None:    
        configs.append("tunnel key {tunnel_key_id}".format(tunnel_key_id=tunnel_key_id)) 
    
    if  next_hop_server_ip is not None and nbma_ip_address is not None:      
        configs.append("ip nhrp nhs {next_hop_server_ip} nbma {nbma_ip_address} multicast".format(next_hop_server_ip=next_hop_server_ip,nbma_ip_address=nbma_ip_address))   
    
    if gre_multipoint:
        configs.append("tunnel mode gre multipoint")
    elif ipsec:
        if dual_overlay is True :
            configs.append("tunnel mode ipsec dual-overlay")
        elif (dual_overlay is False and type == 'ipv4' ):
            configs.append("tunnel mode ipsec ipv4 v6-overlay")
        elif (dual_overlay is False and type == 'ipv6' ):
            configs.append("tunnel mode ipsec ipv6 v4-overlay")
    
    if tunnel_destination is not None:
        configs.append("tunnel destination {tunnel_destination}".format(tunnel_destination=tunnel_destination))
    
    if ipv6_enable:
        configs.append("ipv6 enable")


    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure interface Tunnel spoke,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_interface_tunnel_key(device, tunnel_intf, key):
    """ Configure tunnel key on a tunnel interface
        Args:
            device ('obj'): Device object
            tunnel_intf ('str'): tunnel interface
            key ('int'): tunnel key to configure
        
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {tunnel_intf}')
    cmd.append(f'tunnel key {key}')
    try:
        print(cmd)
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure tunnel key on interface {tunnel_intf}. Error:\n{e}")

def unconfigure_interface_tunnel_key(device, tunnel_intf):
    """ Unconfigure tunnel key on a tunnel interface
        Args:
            device ('obj'): Device object
            tunnel_intf ('str'): tunnel interface
        
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'interface {tunnel_intf}')
    cmd.append('no tunnel key')
    try:
        print(cmd)
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure tunnel key on interface {tunnel_intf}. Error:\n{e}")

def configure_tunnel_mode_gre_multipoint(device, tunnel_intf):
    """ Configure tunnel mode gre multipoint
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):interface to be configured
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure tunnel mode gre multipoint")

    configs=[f"interface {tunnel_intf}",
             "tunnel mode gre multipoint"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure tunnel mode gre multipoint on {tunnel_intf}. Error: {e}')

def unconfigure_tunnel_mode_gre_multipoint(device, tunnel_intf):
    """ Configure tunnel mode gre multipoint
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):interface to be configured
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure tunnel mode gre multipoint")

    configs=[f"interface {tunnel_intf}",
             "no tunnel mode gre multipoint"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure tunnel mode gre multipoint on {tunnel_intf}. Error: {e}')

def configure_tunnel_source(device, interface, tunnel_intf):
    """ Configure tunnel source
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):interface to be configured
            interface('str'):source interface
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure tunnel source")

    configs=[f"interface {tunnel_intf}",
             f"tunnel source {interface}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure tunnel source on {tunnel_intf}. Error: {e}')

def unconfigure_tunnel_source(device, interface, tunnel_intf):
    """ Configure tunnel source
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):interface to be configured
            interface('str'):source interface
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure tunnel source")

    configs=[f"interface {tunnel_intf}",
             f"no tunnel source {interface}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure tunnel source on {tunnel_intf}. Error: {e}')


def configure_ip_nhrp_network_id(device, tunnel_intf, num):
    """ Configure ip nhrp network id
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):interface to be configured
            num('int'):network id
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp network id")

    configs=[f"interface {tunnel_intf}",
             f"ip nhrp network-id {num}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure ip nhrp network id on {tunnel_intf}. Error: {e}')

def unconfigure_ip_nhrp_network_id(device, tunnel_intf, num):
    """ Configure ip nhrp network id
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):interface to be configured
            num('int'):network id
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp network id")

    configs=[f"interface {tunnel_intf}",
             f"no ip nhrp network-id {num}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ip nhrp network id on {tunnel_intf}. Error: {e}')

def configure_ip_nhrp_redirect(device, tunnel_intf):
    """ Configure ip nhrp redirect
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):interface to be configured
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp redirect")

    configs=[f"interface {tunnel_intf}",
             "ip nhrp redirect"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure ip nhrp redirect on {tunnel_intf}. Error: {e}')

def unconfigure_ip_nhrp_redirect(device, tunnel_intf):
    """ Configure ip nhrp redirect
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):interface to be configured
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp redirect")

    configs=[f"interface {tunnel_intf}",
             "no ip nhrp redirect"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ip nhrp redirect on {tunnel_intf}. Error: {e}')

def configure_ip_nhrp_map(device, tunnel_intf, tunnel_ip, nbma_address):
    """ Configure ip nhrp map
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            tunnel_ip('str'):tunnel ip address of destination
            nbma_address('str'):nbma address of destination
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp map")

    configs=[f"interface {tunnel_intf}",
             f"ip nhrp map {tunnel_ip} {nbma_address}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure ip nhrp map on {tunnel_intf}. Error: {e}')

def unconfigure_ip_nhrp_map(device, tunnel_intf, tunnel_ip, nbma_address):
    """ Configure ip nhrp map
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            tunnel_ip('str'):tunnel ip address of destination
            nbma_address('str'):nbma address of destination
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp map")

    configs=[f"interface {tunnel_intf}",
             f"no ip nhrp map {tunnel_ip} {nbma_address}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ip nhrp map on {tunnel_intf}. Error: {e}')

def configure_ip_nhrp_map_multicast(device, tunnel_intf, nbma_address):
    """ Configure ip nhrp map multicast
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            nbma_address('str'):nbma address of destination
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp map multicast")

    configs=[f"interface {tunnel_intf}",
             f"ip nhrp map multicast {nbma_address}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure ip nhrp map multicast on {tunnel_intf}. Error: {e}')

def unconfigure_ip_nhrp_map_multicast(device, tunnel_intf, nbma_address):
    """ Configure ip nhrp map multicast
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            nbma_address('str'):nbma address of destination
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp map multicast")

    configs=[f"interface {tunnel_intf}",
             f"no ip nhrp map multicast {nbma_address}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ip nhrp map multicast on {tunnel_intf}. Error: {e}')

def configure_ip_nhrp_nhs(device, tunnel_intf, tunnel_ip ):
    """ Configure ip nhrp nhs
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            tunnel_ip('str'):tunnel ip address of destination
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp nhs")

    configs=[f"interface {tunnel_intf}",
             f"ip nhrp nhs {tunnel_ip}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure ip nhrp nhs on {tunnel_intf}. Error: {e}')

def unconfigure_ip_nhrp_nhs(device, tunnel_intf, tunnel_ip ):
    """ Configure ip nhrp nhs
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            tunnel_ip('str'):tunnel ip address of destination
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp nhs")

    configs=[f"interface {tunnel_intf}",
             f"no ip nhrp nhs {tunnel_ip}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ip nhrp nhs on {tunnel_intf}. Error: {e}')

def configure_ip_nhrp_authentication(device, tunnel_intf, test):
    """ Configure ip nhrp authentication
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            test('str'):test name
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp authentication")

    configs=[f"interface {tunnel_intf}",
             f"ip nhrp authentication {test}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure ip nhrp authentication on {tunnel_intf}. Error: {e}')

def unconfigure_ip_nhrp_authentication(device, tunnel_intf, test):
    """ Configure ip nhrp authentication
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            test('str'):test name
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp authentication")

    configs=[f"interface {tunnel_intf}",
             f"no ip nhrp authentication {test}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ip nhrp authentication on {tunnel_intf}. Error: {e}')

def configure_nhrp_group(device, tunnel_intf, group):
    """ Configure nhrp group
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            group('str'):nhrp group
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure nhrp group")

    configs=[f"interface {tunnel_intf}",
             f"nhrp group {group}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure nhrp group on {tunnel_intf}. Error: {e}')

def unconfigure_nhrp_group(device, tunnel_intf, group):
    """ Configure nhrp group
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            group('str'):nhrp group
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure nhrp group")

    configs=[f"interface {tunnel_intf}",
             f"no nhrp group {group}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure nhrp group on {tunnel_intf}. Error: {e}')

def configure_ip_nhrp_holdtime(device, tunnel_intf, time):
    """ Configure ip nhrp holdtime
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            time('int'):time
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp holdtime")

    configs = [f"interface {tunnel_intf}",
               f"ip nhrp holdtime {time}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure ip nhrp holdtime on {tunnel_intf}. Error: {e}')

def unconfigure_ip_nhrp_holdtime(device, tunnel_intf, time):
    """ Configure ip nhrp holdtime
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
            time('int'):time
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp holdtime")

    configs = [f"interface {tunnel_intf}",
               f"no ip nhrp holdtime {time}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ip nhrp holdtime on {tunnel_intf}. Error: {e}')

def configure_ip_nhrp_map_multicast_dynamic(device, tunnel_intf):
    """ Configure ip nhrp map multicast dynamic
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp map multicast dynamic")

    configs = [f"interface {tunnel_intf}",
               "ip nhrp map multicast dynamic"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not Configure ip nhrp map multicast dynamic on {tunnel_intf}. Error: {e}')
    
def unconfigure_ip_nhrp_map_multicast_dynamic(device, tunnel_intf):
    """ Configure ip nhrp map multicast dynamic
        Args:
            device (`obj`): Device object
            tunnel_intf('str'):tunnel interface to be configured
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure ip nhrp map multicast dynamic")

    configs = [f"interface {tunnel_intf}",
               "no ip nhrp map multicast dynamic"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure ip nhrp map multicast dynamic on {tunnel_intf}. Error: {e}')

def configure_dmvpn_tunnel(device,
                            tunnel,
                            bandwidth=None,
                            delay=None,
                            ivrf=None,
                            fvrf=None,
                            ip_type="ipv4",
                            address_ipv4=None,
                            mask_ipv4=None,
                            address_ipv6=None,
                            mask_ipv6=None,
                            tunnel_source=None,
                            tunnel_key=None,
                            tunnel_mode=None,
                            tunnel_pmtu=False,
                            tunnel_protection_profile=None,
                            tunnel_protection_profile_shared=False,
                            nhrp_holdtime=None,
                            nhrp_authentication=None,
                            nhrp_network_id=None,
                            nhrp_redirect=True,
                            nhrp_nhs=None,
                            nhrp_nbma=None,
                            nhrp_nhs_nbma_multicast=None,
                            nhrp_nhs_nbma_cluster=None,
                            nhrp_nhs_nbma_priority=None,
                            nhrp_map_group=None,
                            nhrp_map_group_service_policy=None,
                            nhrp_group=None,
                            bfd_enable=False,
                            bfd_interval=None,
                            bfd_min_rx=None,
                            bfd_multiplier=None,
                            ):
    """ Configures DMVPN tunnel interface
        Args:
            device ('obj'): Device object
            tunnel ('str'): Tunnel interface name
            bandwidth ('int', optional): Bandwidth in kbps
            delay ('int', optional): Delay in microseconds
            ivrf ('str', optional): Internal VRF name(vrf forwarding)
            fvrf ('str', optional): Forwarding VRF name(tunnel vrf)
            ip_type ('str', optional): IP type, either 'ipv4', 'ipv6' or 'dual'
            address_ipv4 ('str', optional): IPv4 address
            mask_ipv4 ('str', optional): IPv4 mask
            address_ipv6 ('str', optional): IPv6 address
            mask_ipv6 ('str', optional): IPv6 mask
            tunnel_source ('str', optional): Tunnel source interface or IP address
            tunnel_key ('int', optional): Tunnel key
            tunnel_mode ('str', optional): Tunnel mode, either 'gre multipoint', gre multipoint ipv6', 'ipsec dual-overlay', 'ipsec ipv4 v6-overlay', or 'ipsec ipv6 v4-overlay'
            tunnel_pmtu ('bool', optional): Enable PMTU discovery
            tunnel_protection_profile ('str', optional): IPSEC profile name for tunnel protection
            tunnel_protection_profile_shared ('bool', optional): Use shared IPSEC profile for tunnel protection
            nhrp_holdtime ('int', optional): NHRP hold time in seconds
            nhrp_authentication ('str', optional): NHRP authentication string
            nhrp_network_id ('int', optional): NHRP network ID
            nhrp_redirect ('bool', optional): Enable NHRP redirects
            nhrp_nhs ('str', optional): NHRP Next Hop Server IP address
            nhrp_nbma ('str', optional): NHRP NBMA address
            nhrp_nhs_nbma_multicast ('str', optional): NHRP NHS NBMA multicast address
            nhrp_nhs_nbma_cluster ('str', optional): NHRP NHS NBMA cluster address
            nhrp_nhs_nbma_priority ('int', optional): NHRP NHS NBMA priority
            nhrp_map_group ('str', optional): NHRP map group name(qos)
            nhrp_map_group_service_policy ('str', optional): NHRP map group service policy name(qos)
            nhrp_group ('str', optional): NHRP group name(qos)
            bfd_enable ('bool', optional): Enable BFD
            bfd_interval ('int', optional): BFD interval in milliseconds
            bfd_min_rx ('int', optional): BFD minimum receive interval in milliseconds
            bfd_multiplier ('int', optional): BFD multiplier
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring DMVPN tunnel interface")
    configs = [f"interface {tunnel}"]
    if bandwidth:
        configs.append(f"bandwidth {bandwidth}")
    if delay:
        configs.append(f"delay {delay}")
    if ivrf:
        configs.append(f"vrf forwarding {ivrf}")
    if fvrf:
        configs.append(f"tunnel vrf {fvrf}")
    if ip_type == "ipv6" or ip_type == "dual":
        configs.append("ipv6 enable")
    if address_ipv4 and mask_ipv4:
        configs.append(f"ip address {address_ipv4} {mask_ipv4}")
    if address_ipv6 and mask_ipv6:
        configs.append(f"ipv6 address {address_ipv6}/{mask_ipv6}")
    if tunnel_source:
        configs.append(f"tunnel source {tunnel_source}")
    if tunnel_key:
        configs.append(f"tunnel key {tunnel_key}")
    if tunnel_mode:
        configs.append(f"tunnel mode {tunnel_mode}")
    if tunnel_pmtu:
        configs.append("tunnel path-mtu-discovery")
    if tunnel_protection_profile:
        if tunnel_protection_profile_shared:
            configs.append(f"tunnel protection ipsec profile {tunnel_protection_profile} shared")
        else:
            configs.append(f"tunnel protection ipsec profile {tunnel_protection_profile}")
        
    if nhrp_holdtime:
        if ip_type == "ipv4" or ip_type == "dual":
            configs.append(f"ip nhrp holdtime {nhrp_holdtime}")
        elif ip_type == "ipv6" or ip_type == "dual":
            configs.append(f"ipv6 nhrp holdtime {nhrp_holdtime}")
    if nhrp_authentication:
        if ip_type == "ipv4" or ip_type == "dual":
            configs.append(f"ip nhrp authentication {nhrp_authentication}")
        elif ip_type == "ipv6" or ip_type == "dual":
            configs.append(f"ipv6 nhrp authentication {nhrp_authentication}")
    if nhrp_network_id:
        if ip_type == "ipv4" or ip_type == "dual":
            configs.append(f"ip nhrp network-id {nhrp_network_id}")
        elif ip_type == "ipv6" or ip_type == "dual":
            configs.append(f"ipv6 nhrp network-id {nhrp_network_id}")
    if nhrp_redirect:
        if ip_type == "ipv4" or ip_type == "dual":
            configs.append("ip nhrp redirect")
        elif ip_type == "ipv6" or ip_type == "dual":
            configs.append("ipv6 nhrp redirect")
    if nhrp_nhs:
        if nhrp_nbma:
            cluster = ""
            multicast = ""
            priority = ""
            if nhrp_nhs_nbma_cluster:
                cluster = f"nbma {nhrp_nhs_nbma_cluster}"
            if nhrp_nhs_nbma_multicast:
                multicast = "multicast"
            if nhrp_nhs_nbma_priority:
                priority = f"priority {nhrp_nhs_nbma_priority}"
            if ip_type == "ipv4" or ip_type == "dual":
                configs.append(f"ip nhrp nhs {nhrp_nhs} nbma {nhrp_nbma} {multicast} {cluster} {priority}")
            elif ip_type == "ipv6" or ip_type == "dual":
                configs.append(f"ipv6 nhrp nhs {nhrp_nhs} nbma {nhrp_nbma} {multicast} {cluster} {priority}")
    if nhrp_map_group and nhrp_map_group_service_policy:
        configs.append(f"nhrp map group {nhrp_map_group} service-policy output {nhrp_map_group_service_policy}")
    if nhrp_group:
        configs.append(f"nhrp group {nhrp_group}")
    if bfd_enable:
        configs.append("bfd enable")
    if bfd_interval and bfd_min_rx and bfd_multiplier:
        configs.append(f"bfd interval {bfd_interval} min_rx {bfd_min_rx} multiplier {bfd_multiplier}")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(f"Failed to configure DMVPN tunnel interface {tunnel}, Error:\n{e}")
        raise SubCommandFailure(f"Failed to configure DMVPN tunnel interface {tunnel}. Error:\n{e}")
