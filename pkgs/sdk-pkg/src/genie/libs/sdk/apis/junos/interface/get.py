"""Common get info functions for OSPF"""

# Python
import re
import logging
import copy
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils import Dq
# Pyats
from pyats.utils.objects import find, R

# unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_interface_address_mask_running_config(
        device, interface, address_family):
    """ Get interface address and mask from show running-config interface {interface}
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            address_family ('str'): Address family

        Returns:
            (Interface IP address, Interface Mask)

        Raise:
            None
    """
    try:
        output = device.execute('show configuration interfaces {interface}'
                                .format(interface=interface))
    except SubCommandFailure:
        return None, None

    if not output:
        return None, None

    if address_family in ['ipv4', 'inet']:
        # address 192.168.0.1/32
        p1 = re.compile(r'address +(?P<ip>[\d\.]+)/(?P<mask>\d+);')
    elif address_family in ['ipv6', 'inet6']:
        # address 2001:db8:1005:4401::b/128
        p1 = re.compile(r'address +(?P<ip>[\w\:]+)/(?P<mask>\d+);')
    else:
        log.info(
            'Must provide one of the following address families: "ipv4", "ipv6", "inet", "inet6"')
        return None, None

    match = p1.findall(output)
    if match:
        return match[0][0], device.api.int_to_mask(int(match[0][1]))

    return None, None


def get_interface_ip_address(device, interface, address_family,
                             return_all=False):
    """ Get interface ip address from device

        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object
            address_family ('str'): Address family
            return_all ('bool'): return List of values
        Returns:
            None
            ip_address ('str'): If has multiple addresses
                                will return the first one.

        Raises:
            None
    """
    if address_family not in ["ipv4", "ipv6", "inet", "inet6"]:
        log.info('Must provide one of the following address families: '
                 '"ipv4", "ipv6", "inet", "inet6"')
        return

    if address_family == "ipv4":
        address_family = "inet"
    elif address_family == "ipv6":
        address_family = "inet6"

    try:
        out = device.parse('show interfaces terse {interface}'.format(
            interface=interface))
    except SchemaEmptyParserError:
        return

    # Example dictionary structure:
    #         {
    #             "ge-0/0/0.0": {
    #                 "protocol": {
    #                     "inet": {
    #                         "10.189.5.93/30": {
    #                             "local": "10.189.5.93/30"
    #                         }
    #                     },
    #                     "inet6": {
    #                         "2001:db8:223c:2c16::1/64": {
    #                             "local": "2001:db8:223c:2c16::1/64"
    #                         },
    #                         "fe80::250:56ff:fe8d:c829/64": {
    #                             "local": "fe80::250:56ff:fe8d:c829/64"
    #                         }
    #                     },
    #                 }
    #             }
    #         }

    found = Dq(out).contains(interface).contains(address_family). \
        get_values("local")
    if found:
        if return_all:
            return found
        return found[0]
    return None
