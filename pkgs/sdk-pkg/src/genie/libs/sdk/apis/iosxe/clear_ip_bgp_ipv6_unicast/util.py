""" Common utility functions for routing"""
# Python
import logging
import ipaddress as ip_addr
import re
from unicon.eal.dialogs import Dialog, Statement
# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)
LOG = log

def clear_ip_bgp_ipv6_unicast(device, address_family=None, route=None):
    """
        clear ip bgp ipv6 unicast {route}
        Args:
            device ('obj'): Device object
            route ('int') :  route value (Ex : 200)
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """

    log.debug("clear ip bgp ipv6 {address_family} {route}".format(address_family=address_family,route=route))

    try:
        device.execute("clear ip bgp ipv6 {address_family} {route}".format(address_family=address_family,route=route))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip bgp ipv6 {address_family} {route} on {device}. Error:\n{error}".format(
                address_family=address_family,route=route,device=device, error=e
            )
        )