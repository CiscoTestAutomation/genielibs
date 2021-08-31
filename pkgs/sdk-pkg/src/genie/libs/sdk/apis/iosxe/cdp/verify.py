"""Common verify functions for cdp"""

# Python
import logging
from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common
log = logging.getLogger(__name__)

def verify_cdp_in_state(device, max_time=60, check_interval=10):
    """ Verify that cdp is enabled on the device
        Args:
            device = device to check status on
        returns:
            True if cdp is enabled, false in all other cases
    """
    timeout = Timeout(max_time, check_interval, True)

    while timeout.iterate():
        try:
            device.parse('show cdp neighbors')
            return True
        except Exception:
            timeout.sleep()
    return False
    
def verify_cdp_peer_interface(device, interfaces, max_time=60, 
                              check_interval=10):
    """ Verify interfaces of peer are present in cdp neighbors
        Args:
            device('obj'): device 
            interfaces(`list`): interfaces to be checked
        returns:
            True if cdp is enabled, false in all other cases
    """
    timeout = Timeout(max_time, check_interval, True)

    while timeout.iterate():
        try:
            output=device.parse('show cdp neighbors')
            neighbor_intf=output.q.get_values('port_id')
            neighbor_intf1=[]
            for intf in interfaces:
                neighbor_intf1.append(Common.convert_intf_name\
                    (intf=intf.strip())) 
            if not (set(neighbor_intf1)-set(neighbor_intf)):
                log.info(
                    "Required interfaces {neighbor_intf1} present in cdp "
                    "neighborship".format(neighbor_intf1=neighbor_intf1))
                return True
            else:
                log.error("Required interface "
                "{set(neighbor_intf1)-set(neighbor_intf)} not found"\
                    .format(neighbor_intf1=neighbor_intf1, 
                            neighbor_intf=neighbor_intf))  
                timeout.sleep()                
        except Exception:
            timeout.sleep()
    return False