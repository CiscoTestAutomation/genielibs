"""Common configure functions for vlan"""

# Python
import logging
# Unicon
from unicon.core.errors import SubCommandFailure
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def configure_ipv6_traffic_filter_acl(device, vlan_range_from, vlan_range_to, acl, direction):
    """Configure an IPv6 address on a vlan

        Args:
            device ('obj'): Device object
            vlan_range_from ('int'): vlan starting range (Ex : 1-4094)
            vlan_range_to ('int'): vlan ending at (Ex : 1-4094)
            acl ('str') : acl type (Ex : ipv6_md_acl)
            direction ('str'): acl direction (Ex : in or out)
        Return:
            None
        Raise:
            SubCommandFailure: Failed to configure Ipv6 address on vlan
    """

    cmd = [f"interface range vlan {vlan_range_from}-{vlan_range_to}",
           f"ipv6 traffic-filter {acl} {direction}"]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure Ipv6 address on range vlan {vlan_range_from}-{vlan_range_to},'
            f'Error: {e}'
        )

def unconfigure_ipv6_traffic_filter_acl(device, vlan_range_from, vlan_range_to, acl, direction):
    """Unconfigure an IPv6 address on a vlan

        Args:
            device ('obj'): Device object
            vlan_range_from ('int'): vlan starting range (Ex : 1-4094)
            vlan_range_to ('int'): vlan ending at (Ex : 1-4094)
            acl ('str') : acl type (Ex : ipv6_md_acl)
            direction ('str'): acl direction (Ex : in or out)
        Return:
            None
        Raise:
            SubCommandFailure: Failed to configure Ipv6 address on vlan
    """

    cmd = [f"interface range vlan {vlan_range_from}-{vlan_range_to}",
           f"no ipv6 traffic-filter {acl} {direction}"]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure Ipv6 address on range vlan {vlan_range_from}-{vlan_range_to}, '
            f'Error: {e}'
        )