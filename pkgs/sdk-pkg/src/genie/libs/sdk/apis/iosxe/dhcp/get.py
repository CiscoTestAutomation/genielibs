"""Common get functions for DHCPv4"""

# Python
import logging

from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_dhcpv4_server_stats(device):
    """Get the dhcpv4 server statistics on device
       Args:
            device('obj'): device object
       Returns:
            parsed output
       Raises:
            SchemaEmptyParserError
    """

    try:
        return device.parse("show ip dhcp server statistics")
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}

def get_dhcpv4_server_bindings(device, vrf=None):
    """Get the dhcpv4 server bindings on device
       Args:
            device('obj'): device object
            vrf (`str`, Optional): vrf name, defaults to None.
       Returns:
            parsed output
       Raises:
            SchemaEmptyParserError
    """

    if vrf:
        cmd = f'show ip dhcp binding vrf {vrf}'
    else:
        cmd = f'show ip dhcp binding'
    try:
        return device.parse(cmd)
    except SchemaEmptyParserError:
        log.debug("Command has not returned any results")
        return {}

def get_dhcpv4_binding_address_list(device, vrf=None):
    """Get the list of all ip addresses in the dhcpv4 binding table
        Args:
            device('obj'): device object with dhcp server configured
            vrf('str', Optional): vrf name, defaults to None
        Returns:
            address_list('list'): list of addresses
        Raises:
            SchemaEmptyParserError
    """
    out = device.api.get_dhcpv4_server_bindings(vrf)
    address_list = []
    if out:
        for client, client_info in out['dhcp_binding'].items():
            address_list.append(client_info['ip_address'])

    return address_list
