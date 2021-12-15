"""Common configure functions for DNS"""


# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ip_domain_lookup(
    device, 
):
    """ Enable domain lookup 
        Args:
            device ('obj'): device to use
        Returns:
            console output
        Raises:
            SubCommandFailure: domian configuration
    """

    cmd = ['ip domain lookup']
    
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure domain lookup. Error:\n{error}'.format(error=e)
        )
    return out

def unconfigure_ip_domain_lookup(
    device, 
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
):
    """ Enable ip name server 
        Args:
            device ('obj'): device to use
            domain_ip ('str'): dns server ip or proxy server ip.
        Returns:
            console output
        Raises:
            SubCommandFailure: domian configuration
    """

    cmd = ["ip name-server {}".format(domain_ip)]

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
):
    """ Disable ip name server
        Args:
            device ('obj'): device to use
            domain_ip ('str'): dns server ip or proxy server ip.
        Returns:
            console output
        Raises:
            SubCommandFailure: domian Unconfiguration
    """

    cmd = ["no ip name-server {}".format(domain_ip)]

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Un-configure ip name server. Error:\n{error}".format(error=e)
        )
    return out

