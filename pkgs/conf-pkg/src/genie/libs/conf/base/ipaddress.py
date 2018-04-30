
__all__ = (
    'IPv4Address',
    'IPv4Interface',
    'IPv4Network',
    'IPv6Address',
    'IPv6Interface',
    'IPv6Network',
    'ip_address',
    'ip_interface',
    'ip_network',
    'IPv4AddressRange',
    'IPv6AddressRange',
    'IPv4InterfaceRange',
    'IPv6InterfaceRange',
)

from ipaddress import IPv4Address, IPv4Interface, IPv4Network
from ipaddress import IPv6Address, IPv6Interface, IPv6Network
from ipaddress import ip_address, ip_interface, ip_network

from genie.conf.base.utils import IPv4AddressRange, IPv6AddressRange
from genie.conf.base.utils import IPv4InterfaceRange, IPv6InterfaceRange

