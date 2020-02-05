"""Common get info functions for OSPF"""

# Python
import re
import logging

# unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_interface_address_mask_running_config(device, interface, address_family):
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
        log.info('Must provide one of the following address families: "ipv4", "ipv6", "inet", "inet6"')
        return None, None

    match = p1.findall(output)
    if match:
        return match[0][0], device.api.int_to_mask(int(match[0][1]))

    return None, None
