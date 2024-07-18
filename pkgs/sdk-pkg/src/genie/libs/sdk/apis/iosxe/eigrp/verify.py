from genie.utils.timeout import Timeout
import logging
import os
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_eigrp_interfaces(
    device,
    vrf="default",
    AS_N=None,
    interfaces_list=None,
    ip="ipv4",
    max_time=60,
    check_interval=10,
):
    """Verify active EIGRP interfaces for ipv4 (Default) or ipv6 for AS and VRF
    Args:
      device (obj): Device object
      vrf = "default" (str): Name of the vrf by default set to "default"
      AS_N = None (int): Autonomous System
      interfaces_list = None (list): List of active EIGRP interfaces to check
      ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6"
      max_time (`int`): Max time, default: 30
      check_interval (`int`): Check interval, default: 10

    Returns:
      True
      False
    """
    assert isinstance(AS_N, int), "AS_N must be int"
    assert isinstance(vrf, str), "vrf must be str"
    assert isinstance(
        interfaces_list, list
    ), "interfaces_list must be list of interfaces"
    assert AS_N != 0, "AS_N must not be 0"
    assert ip in ["ipv4", "ipv6"], "ip must be ipv4 or ipv6"
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if AS_N and interfaces_list:
            try:
                response = device.parse(
                    f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces"
                )
            except SchemaEmptyParserError:
                timeout.sleep()
                continue
            interfaces = []
            if (vrf not in response.q.get_values("vrf")) or (
                str(AS_N) not in response.q.get_values("eigrp_instance")
            ):
                log.error(
                    f"Sorry,no data for the provided 'AS = {AS_N}' and/or 'vrf = {vrf}' !"
                )
            else:
                interfaces = (
                    response.q.contains(vrf)
                    .contains_key_value("eigrp_instance", str(AS_N))
                    .contains(ip)
                    .get_values("interface")
                )
            return set(interfaces_list).issubset(interfaces)
        log.error(
            f"Please, provide a valid format for AS, interfaces_list, ip and/or vrf"
        )
        continue


def verify_eigrp_neighbors(
    device,
    neighbors=None,
    vrf="default",
    AS_N=None,
    ip="ipv4",
    max_time=60,
    check_interval=10,
):
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
    assert AS_N != 0, "AS_N must not be 0"
    assert ip in ["ipv4", "ipv6"], "ip must be ipv4 or ipv6"
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if AS_N and neighbors:
            try:
                response = device.parse(
                    f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp neighbors"
                )
            except SchemaEmptyParserError:
                timeout.sleep()
                continue
            eigrp_neighbors = []
            if (vrf not in response.q.get_values("vrf")) or (
                str(AS_N) not in response.q.get_values("eigrp_instance")
            ):
                log.error(
                    f"Sorry, no data for the provided 'AS = {AS_N}' and/or 'vrf = {vrf}' !"
                )
            else:
                eigrp_neighbors = (
                    response.q.contains_key_value("eigrp_instance", str(AS_N))
                    .contains(vrf)
                    .contains(ip)
                    .get_values("eigrp_nbr")
                )
            return set(neighbors).issubset(eigrp_neighbors)
        log.error(f"Please, provide a valid format for AS, Neighbors, ip and/or vrf")
        continue

def verify_eigrp_router_id(
    device,
    router_id=None,
    vrf="default",
    auto_sys=None,
    ip="ipv4",
    max_time=60,
    check_interval=10,
):
    """verify EIGRP IDs for a given vrf and auto_sys active instance for ipv4 or ipv6
    Args:
      device (obj): Device object
      router_id = None (list): List of router ID to check
      vrf = "default" (str): Name of the vrf by default set to "default"
      auto_sys = None (int) : Autonomous System
      ip = "ipv4" (str): Protocol ip set by default to "ipv4" to change to "ipv6"
      max_time (`int`): Max time, default: 30
      check_interval (`int`): Check interval, default: 10

    Returns:
      True
      False
    """
    assert isinstance(auto_sys, int), "auto_sys must be int"
    assert isinstance(vrf, str), "vrf must be str"
    assert isinstance(router_id, list), "router_id must be list of router IDs"
    assert auto_sys != 0, "auto_sys must not be 0"
    assert ip in ["ipv4", "ipv6"], "ip must be ipv4 or ipv6"
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if auto_sys and router_id:
            try:
                response = device.parse(
                    f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp topology"
                )
            except SchemaEmptyParserError:
                timeout.sleep()
                continue
            eigrp_id = []
            if (vrf not in response.q.get_values("vrf")) or (
                str(auto_sys) not in response.q.get_values("eigrp_instance")
            ):
                log.error(
                    f"Sorry, no data for the provided for 'auto_sys = {auto_sys}' and/or 'vrf = {vrf}'"
                )
            else:
                eigrp_id = (
                    response.q.contains_key_value("eigrp_instance", str(auto_sys))
                    .contains(vrf)
                    .contains((ip[0:2]).upper() + ip[2:])
                    .get_values("eigrp_id")
                )
            return set(router_id).issubset(eigrp_id)
        log.error(f"Please, provid a valid format for auto_sys, router_id, vrf and/or ip")
        continue

def verify_eigrp_interfaces_timers(
    device,
    timers_dict=None,
    vrf="default",
    auto_sys=None,
    ip="ipv4",
    max_time=60,
    check_interval=10,
):
    """Verify hello interval and hold time of interfaces for a given vrf and active auto_sys for ipv4 or ipv6
    Args:
      device (obj): Device object
      timers_dict (dict): dict to verify containing interfaces with their hello interval and hold time
         # ex.) timers_dict = {'FastEthernet0/0': [{'hello_interval': 5}, {'hold_time': 15}]}
      vrf (str) : Name of the vrf by default set to "default"
      auto_sys (int) : Autonomous System
      ip (str): Protocol ip, default: "ipv4" to change to "ipv6"
      max_time (`int`): Max time, default: 30
      check_interval (`int`): Check interval, default: 10
    Returns:
      result (bool): Verified result
    """
    assert isinstance(auto_sys, int), "auto_sys must be int"
    assert isinstance(vrf, str), "vrf must be str"
    assert isinstance(timers_dict, dict), "timers_dict must be dict"
    assert auto_sys != 0, "auto_sys must not be 0"
    assert ip in ["ipv4", "ipv6"], "ip must be ipv4 or ipv6"
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if auto_sys and timers_dict:
            try:
                response = device.parse(
                    f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces detail"
                )
            except SchemaEmptyParserError:
                timeout.sleep()
                continue
            inter_timers = {}
            if (vrf not in response.q.get_values("vrf")) or (
                str(auto_sys) not in response.q.get_values("eigrp_instance")
            ):
                log.error(
                    f"Sorry, no data for the provided for 'auto_sys = {auto_sys}' and/or 'vrf = {vrf}'"
                )
            else:
                interfaces = (
                    response.q.contains(vrf)
                    .contains_key_value("eigrp_instance", str(auto_sys))
                    .contains(ip)
                    .get_values("interface")
                )
                for interface in interfaces:
                    hello_interval = {
                        "hello_interval": (
                            response.q.contains(interface).get_values("hello_interval")
                        )[0]
                    }
                    hold_time = {
                        "hold_time": (
                            response.q.contains(interface).get_values("hold_time")
                        )[0]
                    }
                    inter_timers[interface] = [hello_interval, hold_time]
            return set(timers_dict).issubset(inter_timers)
        log.error(
            f"Please, provide a valid format for auto_sys, timers_dict, vrf and/or ip"
        )
        continue
        
def verify_eigrp_interfaces_peers(
    device,
    peers_dict=None,
    vrf="default",
    auto_sys=None,
    ip="ipv4",
    max_time=60,
    check_interval=10,
):
    """Verify interfaces and number of EIGRP peers for a given vrf/active auto_sys
    Args:
      device (obj): Device object
      peers_dict (dict): dict of interfaces and the peers
         # ex.) peers_dict = {'FastEthernet0/0': 1}
      vrf (str) : Name of the vrf by default set to "default"
      auto_sys (int) : Autonomous System
      ip (str): Protocol ip, default: "ipv4" to change to "ipv6"
      max_time (`int`): Max time, default: 30
      check_interval (`int`): Check interval, default: 10
    Returns:
      result (bool): Verified result
    """
    assert isinstance(auto_sys, int), "auto_sys must be int"
    assert isinstance(peers_dict, dict), "peers_dict must be dict"
    assert isinstance(vrf, str), "vrf must be str"
    assert auto_sys != 0, "auto_sys must not be 0"
    assert ip in ["ipv4", "ipv6"], "ip must be ipv4 or ipv6"
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if auto_sys and peers_dict:
            try:
                response = device.parse(
                    f"show {'ipv6' if ip!='ipv4' else 'ip'} eigrp interfaces"
                )
            except SchemaEmptyParserError:
                timeout.sleep()
                continue
            inter_peers = {}
            if (vrf not in response.q.get_values("vrf")) or (
                str(auto_sys) not in response.q.get_values("eigrp_instance")
            ):
                log.error(
                    f"Sorry, no data for the provided 'auto_sys = {auto_sys}' and/or 'vrf = {vrf}'"
                )
            else:
                interfaces = (
                    response.q.contains(vrf)
                    .contains_key_value("eigrp_instance", str(auto_sys))
                    .contains(ip)
                    .get_values("interface")
                )
                peers = (
                    response.q.contains(vrf)
                    .contains_key_value("eigrp_instance", str(auto_sys))
                    .contains(ip)
                    .get_values("peers")
                )
                for interface in interfaces:
                    inter_peers = dict(zip(interfaces, peers))
            return all(item in inter_peers.items() for item in peers_dict.items())
        log.error(
            f"Please, provide a valid format for auto_sys, peers_dict, vrf and/or ip"
        )
        continue
