"""Common verify functions for PBR"""

# Python
import logging



# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_route_map(
        device,
        route_map_name,
        expected_acl_name,
        expected_ip_next_hop,
        pbr_sequence_num,
        max_time=15,
        check_interval=5
):
    """ Verify acl usage
        Args:
            device (`obj`): Device object
            route_map_name (`str`): Route map name
            expected_acl_name (`str`): Access-list name
            expected_ip_next_hop (`str`): Next-hop ip
            pbr_sequence_num (`str`): PBR Sequence number
            max_time ('int',optional): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (`int`, optional): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show route-map {route_map}".format(route_map=route_map_name))
        except SchemaEmptyParserError:
            pass

        if out:
            get_acl_name = out[route_map_name]['statements'][pbr_sequence_num]['conditions']['match_access_list']
            get_ip_next_hop = out[route_map_name]['statements'][pbr_sequence_num]['actions']['set_next_hop'][0]

            if (expected_acl_name == get_acl_name) and (expected_ip_next_hop == get_ip_next_hop):
                return True
            else:
                return False
        timeout.sleep()
    return False

def verify_tunnel_status(
        device,
        tunnel_id,
        expected_tunnel_status='up',
        max_time=15,
        check_interval=5
):
    """ Verify acl usage
        Args:
            device (`obj`): Device object
            tunnel_id (`str`): Tunnel id
            expected_tunnel_status (`str`): Tunnel status, Default is up
            max_time ('int',optional): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (`int`, optional): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True
            False

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show interfaces {intf}".format(intf=tunnel_id))

        except SchemaEmptyParserError:
            pass
        if out:
            get_line_protocol = out.q.get_values("line_protocol")[0]
            get_tunnel_oper_status = out.q.get_values("oper_status")[0]

            if (get_line_protocol == expected_tunnel_status) \
                    and (get_tunnel_oper_status == expected_tunnel_status):
                return True
            else:
                return False

        timeout.sleep()
    return False

def verify_tunnel_stats(
        device,
        tunnel_id,
        direction,
        tx_packets,
        pkt_rate,
        max_time=3,
        check_interval=5
):
    """ Verify acl usage
        Args:
            device (`obj`): Device object
            tunnel_id (`str`): Tunnel id
            direction (`str`): Traffic direction
            tx_packets (`int`): Transmit packets
            pkt_rate (`str`): Frames per seconds
            max_time ('int',optional): Maximum wait time for the trigger,
                            in second. Default: 3
            check_interval (`int`, optional): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True
            False

    """
    out = None
    try:
        out = device.parse("show interfaces {intf} stats".format(intf=tunnel_id))
    except SchemaEmptyParserError:
        pass
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if out:
            get_packet_count_in = out[tunnel_id]['switching_path']['distributed_cache']['pkts_in']
            get_packet_count_out = out[tunnel_id]['switching_path']['distributed_cache']['pkts_out']

            expected_max_pkts = tx_packets + int(pkt_rate)
            expected_min_pkts = tx_packets - int(pkt_rate)

            if direction == 'egress':
                if not get_packet_count_out > 0:
                    return False
                if (get_packet_count_out >= expected_min_pkts) and (get_packet_count_out <= expected_max_pkts):
                    return True

            if direction == 'ingress':
                if not get_packet_count_in > 0:
                    return False
                if (get_packet_count_in >= expected_min_pkts) and (get_packet_count_in <= expected_max_pkts):
                    return True
        timeout.sleep()

    return False
