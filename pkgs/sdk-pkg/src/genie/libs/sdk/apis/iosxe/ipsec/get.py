"""Common get info functions for ipsec"""
import logging
from genie.libs.parser.utils.common import Common
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from unicon.core.errors import SubCommandFailure
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

def get_monitor_event_trace_crypto_ipsec_event_from_boot_detail(device, timeout=30):
    """Execute 'show monitor event-trace crypto ipsec event from-boot detail' command
    
    Args:
        device (obj): Device object
        timeout (int, optional): Timeout for command execution in seconds. Default is 30
        
    Returns:
        str: Command output string
        
    Raises:
        SubCommandFailure: If command execution fails
    """
    cmd = "show monitor event-trace crypto ipsec event from-boot detail"
    try:
        output = device.execute(cmd, timeout=timeout)
        return output
    except SubCommandFailure as e:
        log.error(f"Failed to execute '{cmd}' command on {device}. Error:\n{e}")
        raise SubCommandFailure(
            f"Failed to execute '{cmd}' command on {device}. Error:\n{e}"
        )
