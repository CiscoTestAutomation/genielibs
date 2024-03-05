import logging
import os
from genie.metaparser.util.exceptions import SchemaEmptyParserError
log = logging.getLogger(__name__)
from genie.utils.timeout import Timeout

def verify_eigrp_interfaces(device, vrf='default', AS_N=None, interfaces_list=None ,ip='ipv4',max_time=60, check_interval=10):
   """Verify active EIGRP interfaces for ipv4 (Default) or ipv6 for AS and VRF
      Args:
        device (obj): Device object
        vrf = "default" (str): Name of the vrf by default set to "default"
        AS_N = None (int): Autonomous System
        ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6"  
        interfaces_list = None (list): List of active EIGRP interfaces to check 
      Returns:
        Result (`bool`): Verified result with True or False
   """
   timeout = Timeout(max_time, check_interval)
   while timeout.iterate():
      if ((isinstance(AS_N, int) and isinstance(interfaces_list, list) and isinstance (ip, str) and isinstance(vrf, str) and AS_N!=0 and ip in ['ipv4','ipv6'])):

         if AS_N and interfaces_list:
            try:
               response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces")
            except SchemaEmptyParserError:
               return None
            interfaces = []
            if (vrf not in response.q.get_values("vrf")) or (str(AS_N) not in response.q.get_values("eigrp_instance")):
               log.error(f"Sorry,no data for the provided 'AS = {AS_N}' and/or 'vrf = {vrf}' !")
            else:
               interfaces = response.q.contains(vrf).contains_key_value("eigrp_instance", str(AS_N)).contains(ip).get_values('interface')
            Result = set(interfaces_list).issubset(interfaces)
            timeout.sleep()   
         return Result
      else:
         log.error(f"Please, provide a valide format for AS, interfaces_list, ip and/or vrf!!")
         break

def verify_eigrp_neighbors(device, Neighbors = None, vrf='default', AS_N=None, ip='ipv4',max_time=60, check_interval=10):
   """Verify active EIGRP neighbors for ipv4 (Default) and ipv6 for AS and VRF
      Args:
        device (obj): Device object
        vrf = "default" (str) : Name of the vrf
        AS_N = None (int) : Autonomous System
        ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6"
        Neighbors = None (list): Active EIGRP neighbors to check
      Returns:
        Result (`bool`): Verified result with True or False
   """
   timeout = Timeout(max_time, check_interval)
   while timeout.iterate():
      if ((isinstance(AS_N, int) and isinstance(Neighbors, list) and isinstance(vrf, str) and AS_N != 0 and ip in ['ipv4','ipv6'])):
         if AS_N and  Neighbors:
            try:
               response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp neighbors")
            except SchemaEmptyParserError:
               return None
            eigrp_neighbors=[]
            if (vrf not in response.q.get_values("vrf")) or (str(AS_N) not in response.q.get_values("eigrp_instance")):
               log.error(f"Sorry, no data for the provided 'AS = {AS_N}' and/or 'vrf = {vrf}' !")
               return None
            else:
               eigrp_neighbors = response.q.contains_key_value("eigrp_instance",str(AS_N)).contains(vrf).contains(ip).get_values("eigrp_nbr")
            Result = set(Neighbors).issubset(eigrp_neighbors)
            timeout.sleep()   
         return Result
      else:
         log.error(f"Please, provide a valide format for AS, Neighbors, ip and/or vrf!!!!")
         break