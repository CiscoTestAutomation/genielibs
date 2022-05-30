"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

# Genie
from genie.conf.base import Interface
from genie.harness.utils import connect_device

log = logging.getLogger(__name__)

"""Common configure functions for vpdn"""
# Python
import os
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_vpdn_group(device,
        authen_before_forward,
        vpdn_group_number,
        request_dialin,
        accept_dialin,
        domain,
        initiate_to,
        tunnel_hello_interval,
        tunnel_password,
        virtual_template_number,
        local_name):

    """ Configure VPDN

        Args:
            device ('obj'): Device object
            authen_before_forward ('bool') : True or Flase on authentication
            vpdn_group_number ('int') : VPDN group number
            request_dialin ('bool') : True or False for request-dialin
            accept_dialin ('bool') : True or False for request-dialin
            domain ('str') : Domain name
            initiate_to ('str') : initiate to ip address
            tunnel_hello_interval ('str') : hello interval
            tunnel_password ('str') : tunnel password
            virtual_template_number ('str') : virtual-template number
            local_name ('str') : vpdn local name

        Returns:
            None
        Raise:
            SubCommandFailure
    """
    cli = []
   
    cli.append("vpdn enable")
    if authen_before_forward:
        cli.append("vpdn authen-before-forward")
    
    cli.append(f"vpdn-group {vpdn_group_number}")
    
    if request_dialin:
        cli.append(f"request-dialin")
        cli.append(f"protocol l2tp")
        cli.append(f"domain {domain}")
        cli.append(f"initiate-to ip {initiate_to}")
    
    if accept_dialin:
        cli.append(f"accept-dialin")
        cli.append(f"protocol l2tp")
        cli.append(f"virtual-template {virtual_template_number}")
        cli.append(f"local name {local_name}")

    cli.append(f"l2tp tunnel hello {tunnel_hello_interval}")
    cli.append(f"l2tp tunnel password 0 {tunnel_password}")
    try:
        out = device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure the vpdn group")

def unconfigure_vpdn_group(device,vpdn_group_number):
    """ Unconfigure VPDN

        Args:
            device ('obj'): Device object
            vpdn_group_number ('int') : VPDN group number
            
        Returns:
            None
        Raise:
            SubCommandFailure
    """
    cli = [f"no vpdn-group {vpdn_group_number}"]
    try:
        out = device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to unconfigure the vpdn group")

