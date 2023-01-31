"""Common verify functions for ipsec"""

import logging
from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common
from genie.metaparser.util.exceptions import SchemaEmptyParserError
log = logging.getLogger(__name__)

def verify_ipsec_tunnel_status( device, 
    interface, 
    max_time=5, 
    check_interval=1,  
    status='UP-ACTIVE', 
):
    """Verify ipsec tunnel status 
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
            status (`str`): ipsec tunnel status (default is UP-ACTIVE)
        Returns:
            result(`bool`): True if is up else False
    """
    timeout = Timeout(max_time, check_interval)
    interface = Common.convert_intf_name(interface)
    while timeout.iterate():
        try:
            cmd = 'show crypto session interface {interface} detail'.format(
                interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        tunnel_status = out['interface'][interface]['session_status']
        if tunnel_status.lower() == status.lower():
            return True
        timeout.sleep()

    return False