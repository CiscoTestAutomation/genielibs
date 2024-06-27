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

def verify_total_cdp_entries_displayed_interfaces(device, 
    expected_total_cdp_entries_displayed, 
    max_time=60, 
    check_interval=10):
    ''' Check Total cdp entries displayed value
        Args:
            device ('obj'): Device object
            Total cdp entries displayed ('int'): integer value of Total cdp entries displayed 
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if expected cdp entries displayed on device
                            or else return Flase
    '''
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        output=device.parse('show cdp neighbors detail')
        value=output.q.get_values('total_entries_displayed', 0)
        if int(expected_total_cdp_entries_displayed) == (value):
            log.info(" total cdp entries has been correctly displayed i.e '{}'".\
                     format(expected_total_cdp_entries_displayed))
            return True
        else:
            log.error("total cdp entries value '{}' is incorrect".\
                      format(value))
            timeout.sleep()
    return False


def verify_cdp_neighbors_interface(device, interfaces=None, peer_port_id=None, max_time=60,
                              check_interval=10):
    """ Verify interfaces of peer are present in cdp neighbors
        Args:
            device('obj'): device
            interfaces(`list`): interfaces to be checked
            peer_port_id(`str`): specific port_id to check
        returns:
            True if cdp is enabled, false in all other cases
    """
    timeout = Timeout(max_time, check_interval, True)

    while timeout.iterate():
        try:
            if interfaces is None and peer_port_id is None:
                log.error("No interfaces or specific port_id provided for verification.")
                return False

            if peer_port_id:
                   
                intf, port_id = interfaces[0], peer_port_id[0]
                log.info(intf)
                log.info(port_id)
                output_specific = device.parse(f'show cdp neighbors {intf}')
                neighbor_intf_specific = output_specific.q.get_values('port_id')
                                
                if port_id in neighbor_intf_specific:
                    log.info(f"Required peer port_id {port_id} found in cdp neighborship for interface {intf}")
                    return True
                else:
                    log.error(f"Required peer port_id {port_id} not found for interface {intf}")
                    timeout.sleep()

            elif interfaces and len(interfaces) > 1:
                # If a list of interfaces is provided, use 'show cdp neighbors'
                output_general = device.parse('show cdp neighbors')
                neighbor_intf_general = output_general.q.get_values('port_id')
                neighbor_intf_list = [Common.convert_intf_name(intf=intf.strip()) for intf in interfaces]

                if not (set(neighbor_intf_list) - set(neighbor_intf_general)):
                    log.info(
                        f"Required interfaces {neighbor_intf_list} present in cdp "
                        f"neighborship")
                    return True
                else:
                    log.error(f"Required interfaces "
                              f"{set(neighbor_intf_list) - set(neighbor_intf_general)} not found")
                    timeout.sleep()

            else:
                log.error("Invalid interfaces or specific port_id provided for verification.")
                return False

        except Exception:
            timeout.sleep()

    return False