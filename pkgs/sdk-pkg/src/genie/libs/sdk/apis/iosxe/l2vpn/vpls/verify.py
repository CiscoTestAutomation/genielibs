"""Common verification functions for bgp"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout

# Pyats
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# VRF
from genie.libs.sdk.apis.iosxe.vrf.get import get_vrf_interface

# BRIDGE-DOMAIN
from genie.libs.sdk.apis.iosxe.bridge_domain.get import (
    get_bridge_domain_bridge_domain_interfaces,
)

log = logging.getLogger(__name__)


def verify_vpls_same_interface_for_l2vpn_and_l3vpn(
    device, vrf, bridge_domain_id
):
    """ Verify that subinterface for L3VPN vrf and service instance for L2VPN bridge-domain belong to same interface

        Args:
            device('obj'): device object 
            vrf ('str'): vrf name
            bridge_domain_id ('int'): bridge-domain id
        Returns:
            True
            False
        Raises:
            None
    """

    # Get Interfaces using L2VPN vrf name on device uut
    l2vpn_interfaces = []

    l2vpn_interfaces = get_vrf_interface(device=device, vrf=vrf)

    if not l2vpn_interfaces:
        return False

    # Get Interfaces using bridge-domain id on device uut
    l3vpn_interfaces = []
    try:
        l3vpn_interfaces = get_bridge_domain_bridge_domain_interfaces(
            device=device, bridge_domain_id=bridge_domain_id
        )

    except SchemaEmptyParserError as e:
        return False

    if l2vpn_interfaces and l3vpn_interfaces:

        for intf_1 in l2vpn_interfaces:
            # Get interface name by spliting the subinterface name by '.'
            intf_1 = intf_1.split(".")[0]

            for intf_2 in l3vpn_interfaces:
                # Get interface name by spliting the string using space
                intf_2 = intf_2.split(" ")[0]

                if intf_1 == intf_2:

                    log.info(
                        "Subinterface for L3VPN vrf {}"
                        " and service instance for L2VPN bridge-domain {}"
                        " belong to same interface {} for the device {}".format(
                            vrf, bridge_domain_id, intf_1, device.name
                        )
                    )

                    return True

    return False
