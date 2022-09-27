"""Common verification functions for DHCPv4"""

import logging
# Genie
from genie.utils.timeout import Timeout

# Pyats
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)


def verify_dhcpv4_packet_received(device, packet_type, max_time=4,
                                  check_interval=2):
    """Verify a DHCPv4 packet was received
        Args:
            device('obj'): device object
            packet_type('str'): type of dhcpv4 packet
            max_time('int', Optional): maximum time to wait, default 4
            check_interval('int', Optional): how often to check, default 2
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    packet_type = 'dhcp' + packet_type

    while timeout.iterate():
        out = device.api.get_dhcpv4_server_stats()
        if out:
            if packet_type in out['message_received'] and \
                int(out['message_received'][packet_type]) > 0:
                return True
        timeout.sleep()

    log.debug("DHCPv4 {} packet(s) were not received".format(packet_type))
    return False

def verify_dhcpv4_binding_address(device, ip_address,
                                  vrf=None, max_time=20,
                                  check_interval=5):
    """Verify an ipv4 address in present in the DHCPv4
        server binding table
        Args:
            device('obj'): dhcp server object
            ip_address('str'): ip address to find in binding table
            vrf('str', Optional): vrf name, default None
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
            address_list = device.api.get_dhcpv4_binding_address_list(vrf=vrf)
        else:
            address_list = device.api.get_dhcpv4_binding_address_list()

        if address_list and ip_address in address_list:
            return True
        timeout.sleep()

    log.debug("Failed to find ip address in DHCPv4 binding table")
    return False

def verify_dhcp_snooping_glean_enabled(device, max_time=30, interval=10):
    ''' 
    verify_dhcp_snooping_glean_enabled
    Check the output of 'show ip dhcp snooping | include gleaning' to confirm glean is enabled
    Args:
        device ('obj') : Device object
        max_time ('int') : max time to wait
        interval ('int') : interval timer
    Returns:
        True
        False
    Raises:
        None
    '''
    log.info("Executing verify_dhcp_snooping_glean_enabled API")
    timeout = Timeout(max_time=max_time, interval=interval)    
    while timeout.iterate():
        try:
            output = device.parse("show ip dhcp snooping | include gleaning")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        if output['dhcp_snooping_gleaning_status'].get('gleaning_status', '').strip().lower() == 'enabled':
                log.info("Switch DHCP gleaning is enabled")
                return True
        else:
            timeout.sleep()        

    log.info("Switch DHCP gleaning is NOT enabled!")
    return False

def verify_dhcp_snooping_glean_disabled(device, max_time=30, interval=10):
    ''' 
    verify_dhcp_snooping_glean_disabled
    Check the output of 'show ip dhcp snooping | include gleaning' to confirm glean is disabled
    Args:
        device ('obj') : Device object
        max_time ('int') : max time to wait
        interval ('int') : interval timer
    Returns:
        True
        False
    Raises:
        None
    '''
    log.info("Executing verify_dhcp_snooping_glean_disabled API")
    timeout = Timeout(max_time=max_time, interval=interval)    
    while timeout.iterate():
        try:
            output = device.parse("show ip dhcp snooping | include gleaning")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        if output['dhcp_snooping_gleaning_status'].get('gleaning_status', '').strip().lower() == 'disabled':
                log.info("Switch DHCP gleaning is disabled")
                return True
        else:
            timeout.sleep()        

    log.info("Switch DHCP gleaning is NOT disabled!")
    return False