""" Commong utility functions for routing"""

# Python
import logging
import ipaddress as ip_addr
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)
LOG = log


def clear_ip_route(device, route ,vrf=None):
    """
        clear ip route {route}
        clear ip route vrf {vrf} {route} 

        Args:
            device ('obj'): Device object
            route ('str'): ipv4 address
            vrf ('str', optional): vrf name, default=None
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """

    log.debug("Clearing ip route on {device}".format(device=device))

    try:
        if vrf:
            device.execute("clear ip route vrf {vrf} {route}".format(vrf=vrf, route=route))
        else:
            device.execute("clear ip route {route}".format(route=route))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip route {route} on {device}. Error:\n{error}".format(
                device=device, route=route, error=e
            )
        )


def clear_ip_route_all(device, vrf=None):
    """ clear ip route *
        Args:
            device ('obj'): Device object
            vrf ('str'): vrf name, default=None
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """


    log.debug("Clearing ip route on {device}".format(device=device))

    try:
        if vrf:
            device.execute(f"clear ip route vrf {vrf} *")
        else:
            device.execute("clear ip route *")
            
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip route on {device}. Error:\n{error}".format(device=device, error=e)
        )

def ipv6_build_linklocal(device, mac_intf):
    """
    Description:
        Build a link-local IPv6 address from the supplied MAC address.
    Arguments:
        mac ('str'): MAC address to parse
    Returns:
        String containing IPv6 address
    """

    mac = device.api.get_interface_mac_address(mac_intf)
    if not mac:
        log.error("Error: Mac address return is {}".format(mac))
        return None

    linklocal = ''
    try:
        rest = ipv6_build_part_linklocal(mac)
    except Exception as e:
        log.error("Error: An exeception has occured\n{}".format(e))
    if rest is not None:
        linklocal = 'fe80:0000:0000:0000:' + rest
    return ipv6_shorten_address(linklocal)

def ipv6_build_part_linklocal(mac):
    """
    Description:
        Build the lower part of a link-local IPv6 address from the supplied
        MAC address.
    Arguments:
        mac ('str'): MAC address to parse
    Returns:
        String containing the IPv6 address
    """
    # NOTE: bit locations will be relative to the right, with the rightmost bit
    #   being bit 1

    # Chop up mac address into hexadecimal chunks (octet pairs)
    reg = re.compile(r'(?P<a>[\d\w]*)\.(?P<b>[\d\w]*)\.(?P<c>[\d\w]*)')
    m = reg.match(mac)
    if not m:
        # match not found, exit function
        return None
    groups = m.groupdict()
    a, b, c = groups['a'].zfill(4), groups['b'].zfill(4), groups['c'].zfill(4)

    # Invert bit 2 of the first octet (xxxx xxXx xxxx xxxx)
    a = hex(int(a, 16) ^ 512)[2:].zfill(4)

    # Now build up the complete address
    b1, b2 = b[:2], b[2:]     # split middle chunk into two octets
    part = '{}:{}{}:{}{}:{}'.format(a, b1, 'ff', 'fe', b2, c)

    return part.upper()     # make all hex digits lowercase

def ipv6_shorten_address(address):
    """
        Description: 
            Convert IPv6 address into its shortened format.

        Arguments:
            address (str): IPv6 address

        Returns:
            Shortened IPv6 (str) : Shortened IPv6 address

        Example:
            3ffe:0002:0000:0000:0000:0000:0000:0001 -> 3FFE:2::1
    """
    
    addr = ip_addr.ip_address(address)

    return str(addr).upper()

def get_routes_from_parsed(output=None):
    """
    Gets routes from 'show ip route' on a device
    or a parsed dict output.

    Args:
        device (): Device used to run commands
        output ('dict'): Parsed dictionary output from a show cmd

    Returns list of routes and None if exception occurs.
    """
    if not output: 
        LOG.error("Please pass an a parsed dictionary output from show cmd")
        return None
    
    vrf_key = next(iter(output['vrf']))
    route_list = list(output['vrf'][vrf_key]['address_family']['ipv4']['routes'].keys())
    return route_list

def clear_ipv6_route(device, route ,vrf=None):
    """
        clear ipv6 route {route}
        clear ipv6 route vrf {vrf} {route} 

        Args:
            device ('obj'): Device object
            route ('str'): ipv6 address
            vrf ('str', optional): vrf name, default=None
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """

    log.debug("Clearing ipv6 route on {device}".format(device=device))

    try:
        if vrf:
            device.execute("clear ipv6 route vrf {vrf} {route}".format(vrf=vrf, route=route))
        else:
            device.execute("clear ipv6 route {route}".format(route=route))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ipv6 route {route} on {device}. Error:\n{error}".format(
                device=device, route=route, error=e
            )
        )

def clear_ipv6_route_all(device, vrf=None):
    """ clear ipv6 route *
        clear ipv6 route vrf {vrf} *
        Args:
            device ('obj'): Device object
            vrf ('str'): vrf name, default=None
        Returns:
            None
        Raises:
            SubcommandFailure: Failed executing command
    """


    log.debug("Clearing ipv6 routes on {device}".format(device=device))

    try:
        if vrf:
            device.execute(f"clear ipv6 route vrf {vrf} *")
        else:
            device.execute("clear ipv6 route *")
            
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ipv6 route on {device}. Error:\n{error}".format(device=device, error=e)
        )
