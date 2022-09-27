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
            dual_overlay ('boolean',optional) : Setting dual_overlay for tunnel mode ipsec dual-overlay option.Defaults to False.
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