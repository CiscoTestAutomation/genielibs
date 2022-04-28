"""Common configure/unconfigure functions for flexvpn"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_interface_virtual_template(device,
                            virtual_template_interface_number = None,
                            vt_type = None,
                            interface_type = None,
                            interface_number = None,
                            source_interface_type = None,
                            source_interface_number = None,
                            ipsec_profile_name = None,
                            dual_overlay = False, 
                            type = '',
                            ipv6_enable = False,
                            network_id = None,
                            nhrp_redirect = False          
                            ):                            
    """ Configures interface Virtual-Template
        Args:       
            device ('obj'): Device object
            virtual_template_interface_number ('int'): Interface number of the Virtual Template 
            vt_type ('str') : Set Virtual Template type 
            interface_type ('str') : Set Interface type
            interface_number ('int') : Set Interface Number
            source_interface_type ('str',optional) : Interface type of Tunnel Source 
            source_interface_number ('int',optional) : Interface number of Tunnel Source
            ipsec_profile_name ('str',optional): IPSEC profile name
            type ('str',optional) : Type of IP address [Ipv4 or Ipv6]            
            dual_overlay ('boolean',optional) : Setting dual_overlay for tunnel mode ipsec dual-overlay option.Defaults to False.
            network_id  ('int',optional): Network Identifier
            nhrp_redirect ('boolean',optional): Setting ip redirects. Defaults to False. 
            ipv6_enable ('boolean',optional) : Setting ipv6 enable .Defaults to False.

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring interface Virtual_Template"
    )

    configs = []
    configs.append("interface Virtual-Template {virtual_template_interface_number} type {vt_type}".format(virtual_template_interface_number=virtual_template_interface_number,vt_type=vt_type))
    configs.append("ip unnumbered {interface_type} {interface_number}". format(interface_type=interface_type,interface_number=interface_number))

    if source_interface_type is not None and source_interface_number is not None:
        configs.append("tunnel source {source_interface_type} {source_interface_number}". format(source_interface_type=source_interface_type,source_interface_number=source_interface_number))

    if ipsec_profile_name is not None :
        configs.append("tunnel protection ipsec profile {ipsec_profile_name}". format(ipsec_profile_name=ipsec_profile_name))

    if dual_overlay is True :
        configs.append("tunnel mode ipsec dual-overlay")
    elif (dual_overlay is False and type == 'ipv4' ):
        configs.append("tunnel mode ipsec ipv4")
    elif (dual_overlay is False and type == 'ipv6' ):
        configs.append("tunnel mode ipsec ipv6")
    
    if ipv6_enable:
        configs.append("ipv6 enable")

    if network_id is not None:
        configs.append("ip nhrp network-id {network_id}".format(network_id=network_id))      
    
    if nhrp_redirect:
        configs.append("ip nhrp redirect")   

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure interface Virtual-Template"
             "Error:\n{error}".format(error=e)
        )
        raise        