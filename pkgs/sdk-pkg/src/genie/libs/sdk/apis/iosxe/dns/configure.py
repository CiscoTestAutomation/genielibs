"""Common configure functions for DNS"""


# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ip_domain_lookup(
    device,
    source_interface=None,
):
    """ Enable domain lookup 
        Args:
            device ('obj'): device to use
            source_interface ('string', Optional): Name of the interface
        Returns:
            console output
        Raises:
            SubCommandFailure: domian configuration
    """

    cmd = ['ip domain lookup']
    if source_interface:
        cmd.append(f"ip domain lookup source-interface {source_interface}")
    
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure domain lookup. Error:\n{error}'.format(error=e)
        )
    return out

def unconfigure_ip_domain_lookup(
    device, 
    source_interface=None,
):
    """ Disable ip domain lookup 
        Args:
            device ('obj'): device to use
        Returns:
            console output
        Raises:
            SubCommandFailure: domian Unconfiguration
    """
    cmd = ['no ip domain lookup']
    if source_interface:
        cmd.append(f"no ip domain lookup source-interface {source_interface}")

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not Un-configure domain lookup. Error:\n{error}'.format(error=e)
        )
    return out

def configure_ip_name_server(
    device, 
    domain_ip,
    vrf=None,
):
    """ Enable ip name server 
        Args:
            device ('obj'): device to use
            domain_ip ('str'): dns server ip or proxy server ip.
            vrf ('str', Optional): name of the vrf
        Returns:
            console output
        Raises:
            SubCommandFailure: domian configuration
    """
    if vrf:
        cmd = f"ip name-server vrf {vrf} {domain_ip}"
    else:
        cmd = f"ip name-server {domain_ip}"
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ip name server . Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_ip_name_server(
    device, 
    domain_ip,
    vrf=None,
):
    """ Disable ip name server
        Args:
            device ('obj'): device to use
            domain_ip ('str'): dns server ip or proxy server ip.
            vrf ('str', Optional): name of the vrf
        Returns:
            console output
        Raises:
            SubCommandFailure: domian Unconfiguration
    """

    if vrf:
        cmd = f"no ip name-server vrf {vrf} {domain_ip}"
    else:
        cmd = f"no ip name-server {domain_ip}"
        
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Un-configure ip name server. Error:\n{error}".format(error=e)
        )
    return out