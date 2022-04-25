"""Common get functions for DHCPv6"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_dhcpv6_server_stats(device):
    """Get the dhcpv6 server statistics on device
       Args:
            device('obj'): device object
       Returns:
            parsed output
       Raises:
            SubCommandFailure
    """

    try:
        return device.parse("show ipv6 dhcp statistics")
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}


def get_dhcpv6_server_bindings(device, vrf=None):
    """Get the dhcpv6 server bindings on device
       Args:
            device('obj'): device object
            vrf (`str`, optional): vrf name. Defaults to None.
       Returns:
            parsed output
       Raises:
            SchemaEmptyParserError
    """

    if vrf:
        cmd = f'show ipv6 dhcp binding vrf {vrf}'
    else:
        cmd = f'show ipv6 dhcp binding'
    try:
        return device.parse(cmd)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}


def get_dhcpv6_binding_address_list(device, vrf=None):
    """Get the list of all ip addresses in the dhcpv6 binding table
        Args:
            device('obj'): device object with dhcp server configured
            vrf('str', Optional): vrf name
        Returns:
            address_list('list'): list of addresses
        Raises:
            SchemaEmptyParserError
    """
    out = device.api.get_dhcpv6_server_bindings(vrf)
    address_list = []
    if out:
        for client, client_info in out['client'].items():
            if 'ia_na' in client_info:
                for iaid, iaid_info in client_info['ia_na'].items():
                    address_list += list(iaid_info['address'].keys())

    return address_list
