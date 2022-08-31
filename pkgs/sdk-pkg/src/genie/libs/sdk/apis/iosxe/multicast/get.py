"""Common get info functions for multicast"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_ip_mfib_hw_pkts_per_sec(device, multicast_group, source_ip, ip_family, vrf=None ):
    """Gets hw packet counters and others for particular mcast-group 
       along with source ip(if given) in             
       'show ip mfib multicast_group source_ip' - if no vrf, no ip_family
       'show ip mfib vrf <vrf> multicast_group source_ip '- if vrf given and no ip_family
       'show ipv6 mfib multicast_group source_ip' - if ip_family given and no vrf
       'show ipv6 mfib vrf <vrf> multicast_group source_ip' - if both vrf and ip_family given
           ex:
            (1.1.1.1,225.1.1.1) Flags: HW
            SW Forwarding: 0/0/0/0, Other: 11/0/11
            HW Forwarding:   6225553/705/115/634, Other: 0/0/0

    Args:
            device ('obj'): Device object
            multicast_group (`str`): multicast group to be verified
            source_ip ('str'): source_ip to be verified
            ip_family ('str'): either ip or ipv6   
            vrf ('str', optional): vrf        
    Returns:
            result(`str`): verified result
    Raises:
            error incase of incorrect hw field
    """
    if ip_family not in ['ip','ipv6']:
        log.error("Please provide ip_family either as ip or ipv6 only")
        return None
    if vrf:        
        cmd = f"show {ip_family} mfib vrf {vrf} {multicast_group} {source_ip}"
    else:
        cmd = f"show {ip_family} mfib {multicast_group} {source_ip}"
        vrf = 'Default'    

    try:
        out = device.parse(cmd)
    except SchemaEmptyParserError as e:
        log.error(f"Command has not returned any results.\nError: {e}")
        return None

    family_type = 'ipv4' if ip_family == 'ip' else 'ipv6'

    if not out['vrf'][vrf]['address_family'][family_type]:
        log.error(f"No entries for multicast group {multicast_group} with "
            f"source {source_ip}")
        return None
    try:        
        # hw_packets_per_second
        actual_hw_packets_per_second = out['vrf'][vrf]['address_family']\
            [family_type]['multicast_group'][multicast_group]['source_address']\
            [source_ip]['hw_packets_per_second']
        return actual_hw_packets_per_second
    except KeyError as e:
        log.error(f"Unable to grep hw packets per second values.\nError:{e}")
        return None