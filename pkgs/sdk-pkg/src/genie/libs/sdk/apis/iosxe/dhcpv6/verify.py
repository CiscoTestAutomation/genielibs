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

def verify_dhcpv6_packet_received(device, packet_type, prev_output=None,
                                  max_time=4, check_interval=2):
    """Verify a DHCPv6 packet was received
        Args:
            device('obj'): device object
            packet_type('str'): type of dhcpv6 packet
            prev_output('dict', Optional): previous output of 'show ipv6 dhcp stats', default None
            max_time('int', Optional): maximum time to wait, default 4
            check_interval('int', Optional): how often to check, default 2
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    prev_count = 0
    current_count = 0

    while timeout.iterate():
        out = device.api.get_dhcpv6_server_stats()
        if out:
            if prev_output and 'type_received' in prev_output:
                if packet_type in prev_output['type_received']:
                    prev_count = int(prev_output['type_received'][packet_type])

            if 'type_received' in out:
                if packet_type in out['type_received']:
                    current_count = int(out['type_received'][packet_type])

            if current_count > prev_count:
                return True
        timeout.sleep()

    log.debug("Expected more than {} DHCPv6 {} packet(s),"
              " got {}".format(prev_count, packet_type, current_count))
    return False

def verify_dhcpv6_binding_address(device, ipv6_address,
                                  vrf=None, max_time=20,
                                  check_interval=5):
    """Verify an ipv6 address in present in the DHCPv6
        server binding table
        Args:
            device('obj'): dhcp server object
            ipv6_address('str'): ip address to verify in binding table
            vrf('str', Optional): vrf name, default to None
            max_time('int', Optional): maximum time to wait, default 20
            check_interval('int', Optional): how often to check, default 5
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        if vrf:
            address_list = device.api.get_dhcpv6_binding_address_list(vrf=vrf)
        else:
            address_list = device.api.get_dhcpv6_binding_address_list()

        if address_list and ipv6_address in address_list:
            return True
        timeout.sleep()

    log.debug("Failed to find ip address in DHCPv6 binding table")
    return False
