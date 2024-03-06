from genie.utils.timeout import Timeout
import logging
import os
from genie.metaparser.util.exceptions import SchemaEmptyParserError
log = logging.getLogger(__name__)

def verify_eigrp_interfaces(device, vrf='default', AS_N=None, interfaces_list=None ,ip='ipv4',max_time=60, check_interval=10):
    """Verify active EIGRP interfaces for ipv4 (Default) or ipv6 for AS and VRF
       Args:
         device (obj): Device object
         vrf = "default" (str): Name of the vrf by default set to "default"
         AS_N = None (int): Autonomous System
         ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6" 
         interfaces_list = None (list): List of active EIGRP interfaces to check
         max_time (`int`): Max time, default: 30
         check_interval (`int`): Check interval, default: 10

       Returns:
         True
         False
    """
    assert isinstance(AS_N, int), "AS_N must be int"
    assert isinstance(vrf, str), "vrf must be str"
    assert isinstance(interfaces_list, list), "interfaces_list must be list of interfaces"
    assert AS_N!=0, "AS_N must be differt to 0"
    assert ip in ["ipv4","ipv6"], "ip must be ipv4 or ipv6"
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if AS_N and interfaces_list:
            try:
                response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces")
            except SchemaEmptyParserError:
                pass
            interfaces = []
            if (vrf not in response.q.get_values("vrf")) or (str(AS_N) not in response.q.get_values("eigrp_instance")):
                log.error(f"Sorry,no data for the provided 'AS = {AS_N}' and/or 'vrf = {vrf}' !")
            else:
                interfaces = response.q.contains(vrf).contains_key_value("eigrp_instance", str(AS_N)).contains(ip).get_values('interface')
            return set(interfaces_list).issubset(interfaces)
        timeout.sleep()
        log.error(f"Please, provide a valide format for AS, interfaces_list, ip and/or vrf!!")
        break

def verify_eigrp_neighbors(device, neighbors = None, vrf='default', AS_N=None, ip='ipv4',max_time=60, check_interval=10):
    """Verify active EIGRP neighbors for ipv4 (Default) and ipv6 for AS and VRF
       Args:
         device (obj): Device object
         neighbors = None (list): Active EIGRP neighbors to check
         vrf = "default" (str) : Name of the vrf
         AS_N = None (int) : Autonomous System
         ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6"
         max_time (`int`): Max time, default: 30
         check_interval (`int`): Check interval, default: 10 

       Returns:
         True
         False
    """
    assert isinstance(AS_N, int), "AS_N must be int"
    assert isinstance(vrf, str), "vrf must be str"
    assert isinstance(neighbors, list), "neighbors must be list of interfaces"
    assert AS_N!=0, "AS_N must be differt to 0"
    assert ip in ["ipv4","ipv6"], "ip must be ipv4 or ipv6"
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if AS_N and  neighbors:
            try:
                response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp neighbors")
            except SchemaEmptyParserError:
                pass
            eigrp_neighbors=[]
            if (vrf not in response.q.get_values("vrf")) or (str(AS_N) not in response.q.get_values("eigrp_instance")):
                log.error(f"Sorry, no data for the provided 'AS = {AS_N}' and/or 'vrf = {vrf}' !")
            else:
                eigrp_neighbors = response.q.contains_key_value("eigrp_instance",str(AS_N)).contains(vrf).contains(ip).get_values("eigrp_nbr")
            return set(neighbors).issubset(eigrp_neighbors)
        timeout.sleep()
        log.error(f"Please, provide a valide format for AS, Neighbors, ip and/or vrf!!!!")
        break

