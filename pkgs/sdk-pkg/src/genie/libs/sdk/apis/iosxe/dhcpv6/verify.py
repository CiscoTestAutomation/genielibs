"""Common verification functions for DHCPv6"""

# Python
import os
import logging

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# pyATS
from pyats.utils.objects import R, find

# Logger
log = logging.getLogger(__name__)

def verify_ipv6_dhcp_pool(
        device,
        pool_name,
        expected_address_prefix,
        expected_active_clients,
        max_time = 15,
        check_interval = 5
):
    """ Verify ipv6 dhcp pool
        Args:
            device (`obj`): Device object
            pool_name (`str`): IPv6 dhcp pool name
            expected_address_prefix ('str'): Expected IPv6 address prefix
            expected_active_clients ('int'): Expected number of active clients
            max_time ('int',optional): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (`int`, optional): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True : returns true in case of passed scenario
            False : returns false if not expected output
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ipv6 dhcp pool")
        except SchemaEmptyParserError:
            return False

        return (expected_address_prefix, expected_active_clients) == (out[pool_name]['address_allocation_prefix'],
                                                                      out[pool_name]['active_clients'])

    return False
