"""Common verification functions for IPv6"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)

def verify_ipv6_pim_neighbor(device,interface,neighbor_address,max_time=15, check_interval=5):
    """Verify IPv6 PIM neighbor

            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
                neighbor_address ('str'): Neighbor address to be verified
                max_time ('int'): optional, Maximum wait time
                check_interval ('int'): optional, How often to check for output

            Returns:
                True
                False
        """
    interface = Common.convert_intf_name(interface)

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        try:
            out = device.parse("show ipv6 pim neighbor")

        except SchemaEmptyParserError:
            return False

        dev_intf = out["vrf"]["default"]["interfaces"]

        try:
            if interface in dev_intf:
                for intf in dev_intf:
                    dev_neighbor_addr = dev_intf[intf]["address_family"]["ipv6"]["neighbors"]
                    for neighbor in dev_neighbor_addr:
                        if neighbor_address in dev_neighbor_addr and interface in dev_neighbor_addr[neighbor]["interface"]:
                            return True

        except KeyError:
            pass
        timeout.sleep()

    return False
