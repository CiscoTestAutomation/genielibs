# =================================================
# Get APIs for 'EIGRPv4 and EIGRPv6' command
#Author: Mehdi Cherifi
#LinkedIn: https://www.linkedin.com/in/mehdi-cherifi
#Twitter: https://twitter.com/LocketKeepsake
#Github: https://github.com/cherifimehdi
# =================================================

import logging
import os
from genie.metaparser.util.exceptions import SchemaEmptyParserError
log = logging.getLogger(__name__)


def get_eigrp_interfaces(device, vrf='default', AS_N=None, ip='ipv4'):
   """Gets all the interfaces on the device for a given AS and vrf for ipv4 or ipv6 from -show ip eigrp interfaces- for ipv4 by default or -show ipv6 eigrp interfaces- for ipv6

      Args:
        device (obj): Device object
        vrf = "default" (str): Name of the vrf by default set to "default"
        AS_N = None (int): Autonomous System
        ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6"  

      Returns:
        list: List of the interfaces in -interfaces- list
   """

   if ((isinstance(AS_N, int) and isinstance (ip, str) and isinstance(vrf, str) and AS_N!=0 and ip in ['ipv4','ipv6'])):

      if AS_N:
         try:
            response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces")
         except SchemaEmptyParserError:
            return None

         interfaces = []
         if (vrf not in response.q.get_values("vrf")) or (str(AS_N) not in response.q.get_values("eigrp_instance")):
            log.error(f"Sorry,no data for the provided 'AS = {AS_N}' and/or 'vrf = {vrf}' !")
         else:
            interfaces = response.q.contains(vrf).contains_key_value("eigrp_instance", str(AS_N)).contains(ip).get_values('interface')

      return interfaces
   else:
      log.error(f"Please, provide a valide format for AS and/or vrf and ip!!")


def get_eigrp_interfaces_as(device, vrf='default', ip='ipv4'):
   """Gets all the interfaces on the device for a given vrf for ipv4 or ipv6 for all AS active instance from -show ip eigrp interfaces- for ipv4 by default or -show ipv6 eigrp interfaces- for ipv6

      Args:
        device (obj): Device object
        vrf = "default" (str) : Name of the vrf
        ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6" 
        

      Returns:
        Dict: Dctionary of the interfaces for a given AS in -inter_as_dict- Dict
   """
   if (isinstance(vrf, str) and isinstance(ip, str) and  ip in ['ipv4','ipv6']):

      try:
         response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces")
      except SchemaEmptyParserError:
         return None

      inter_as_dict={}
      if (vrf not in response.q.get_values("vrf")):
         log.error(f"Sorry, 'vrf = {vrf}' provided doesn't configured OR doesn't contain eigrp instances!")
         return None
      else:
         as_proc = response.q.contains(vrf).contains(ip).get_values("eigrp_instance")
         for as_n in as_proc:
            interface_as=response.q.contains(as_n).get_values("interface")
            inter_as_dict[as_n]=interface_as

      return inter_as_dict
   else:
      log.error(f"Please, provide a valide format for vrf and/or ip!!")

def get_eigrp_interfaces_timers(device, vrf='default', AS_N=None, ip='ipv4'):

   """Gets hello interval and hold time for the interfaces on the device for a given vrf and AS active instance for ipv4 or ipv6 from -show ip eigrp interfaces detail- for ipv4 or -show ip eigrp interfaces detail- for ipv6

      Args:
        device (obj): Device object
        vrf = "default" (str) : Name of the vrf
        AS_N = None (int) : Autonomous System
        ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6" 
        

      Returns:
        Dict: Dctionary of the timers for all the interfaces for a given AS in -inter_timers- Dict
   """
   if ((isinstance(AS_N, int) and isinstance(vrf, str) and AS_N !=0 and ip in ['ipv4','ipv6'])):
      if AS_N:
         try:
            response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces detail")
         except SchemaEmptyParserError:
            return None

         inter_timers={}
         if (vrf not in response.q.get_values("vrf")) or (str(AS_N) not in response.q.get_values("eigrp_instance")):
            log.error(f"Sorry, no data for the provided for 'AS = {AS_N}' and/or 'vrf = {vrf}' !")
            return None
         else:
            interfaces = response.q.contains(vrf).contains_key_value("eigrp_instance",str(AS_N)).contains(ip).get_values("interface")
            for interface in interfaces:
               hello_interval = {"hello_interval":(response.q.contains(interface).get_values("hello_interval"))[0]}
               hold_time = {"hold_time":(response.q.contains(interface).get_values("hold_time"))[0]}
               inter_timers[interface] = [hello_interval, hold_time]
      return inter_timers
   else:
      log.error(f"Please, provide a valide format for vrf and/or AS and ip!!")

def get_eigrp_interfaces_peers(device, vrf='default', AS_N=None, ip='ipv4'):

   """Gets the interfaces and the number of the EIGRP peers on the device for a given vrf for ipv4 or ipv6 and AS active instance from -show ip eigrp interfaces- for ipv4 or -show ipv6 eigrp interfaces- for ipv6

      Args:
        device (obj): Device object
        vrf = "default" (str) : Name of the vrf
        AS_N = None (int) : Autonomous System
        ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6" 
        

      Returns:
        Dict: Dctionary of the interfaces and the peers for a given AS in -inter_peers- Dict
   """

   if ((isinstance(AS_N, int) and isinstance(vrf, str) and AS_N !=0 and ip in ['ipv4','ipv6'])):
      if AS_N:
         try:
            response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces")
         except SchemaEmptyParserError:
            return None

         inter_peers={}
         if (vrf not in response.q.get_values("vrf")) or (str(AS_N) not in response.q.get_values("eigrp_instance")):
            log.error(f"Sorry, no data for the provided 'AS = {AS_N}' and/or 'vrf = {vrf}' !")
            return None
         else:
            interfaces = response.q.contains(vrf).contains_key_value("eigrp_instance",str(AS_N)).contains(ip).get_values("interface")
            peers = response.q.contains(vrf).contains_key_value("eigrp_instance",str(AS_N)).contains(ip).get_values("peers")
            for interface in interfaces:
               inter_peers=dict(zip(interfaces, peers))
      return inter_peers
   else:
      log.error(f"Please, provide a valide format for vrf and/or AS and ip!!")


def get_eigrp_neighbors(device, vrf='default', AS_N=None, ip='ipv4'):
   """Gets the EIGRP neighbors on the device for a given vrf and AS active instance for ipv4 or ipv6 from -show ip eigrp neighbors- for ipv4 or -show ipv6 eigrp neighbors- for ipv6

      Args:
        device (obj): Device object
        vrf = "default" (str) : Name of the vrf
        AS_N = None (int) : Autonomous System
        ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6" 

      Returns:
        List: List of the EIGRP neighbors for a given AS in -eigrp_neighbors- List
   """
   if ((isinstance(AS_N, int) and isinstance(vrf, str) and AS_N != 0 and ip in ['ipv4','ipv6'])):
      if AS_N:
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

      return eigrp_neighbors
   else:
      log.error(f"Please, provide a valide format for vrf and/or AS and ip!!")

def get_eigrp_router_id(device, vrf='default', AS_N=None, ip = 'ipv4'):
   """Gets the EIGRP IDs on the device for a given vrf and AS active instance for ipv4 or ipv6 from -show ip eigrp topology- for ipv4 or -show ipv6 eigrp topology- for ipv6 

      Args:
        device (obj): Device object
        vrf = "default" (str) : Name of the vrf
        AS_N = None (int) : Autonomous System
        ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6" 

      Returns:
        List: List of the EIGRP IDs for a given AS in -eigrp_id- List
   """
   if AS_N:
      if ((isinstance(AS_N, int) and isinstance(vrf, str) and AS_N != 0 and ip in ['ipv4','ipv6'])):

         try:
            response=device.parse(f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp topology")
         except SchemaEmptyParserError:
            return None

         eigrp_id=[]
         if (vrf not in response.q.get_values("vrf")) or (str(AS_N) not in response.q.get_values("eigrp_instance")):
            log.error(f"Sorry, no data for the provided for 'AS = {AS_N}' and/or 'vrf = {vrf}' !")
            return None
         else:
            eigrp_id = response.q.contains_key_value("eigrp_instance", str(AS_N)).contains(vrf).contains((ip[0:2]).upper()+ip[2:]).get_values("eigrp_id")

      return eigrp_id
   else:
      log.error(f"Please, provide a valide format for vrf and/or AS and ip!!")