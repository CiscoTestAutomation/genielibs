"""Common get info functions for ipsec"""
import logging
from genie.libs.parser.utils.common import Common
from genie.metaparser.util.exceptions import SchemaEmptyParserError
log = logging.getLogger(__name__)


def get_crypto_ipsec_tunnel_counter(
    device,
    interface,
    tunnel_source,
    tunnel_destination,
    counter_field,
):
    """Get interface counters for ipsec tunnel
    Args:
        device ('obj'): device object
        interface ('str'): Interface name
        tunnel_source('str'): Tunnel source IP address
        tunnel_destination('str'): Tunnel destination IP address
        counter_name('str'): Counter/status parameter
    Returns:
        Counter parameter value of an ipsec tunnel
    Raises:
        None
    """
    try:
        interface = Common.convert_intf_name(interface)
        out = device.parse("show crypto session interface {intf} detail".format(intf=interface))
        ipsec_flow1 = out['interface'][interface]['peer'][tunnel_source]['port']['500']['ipsec_flow']
        for host in ipsec_flow1:
            if tunnel_source in host and tunnel_destination in host:
                counter = ipsec_flow1[host].get(counter_field)
                return int(counter)
            else:
                return None
    except SchemaEmptyParserError as e:
        log.error('No ipsec tunnel is configured'
                "Error:\n{error}".format(error=e)
        )
        return None