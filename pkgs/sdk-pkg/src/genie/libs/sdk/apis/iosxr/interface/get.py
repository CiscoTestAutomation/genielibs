"""Common get info functions for interface"""

# Python
import re
import logging

# unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)


def get_interface_ip_address(device, interface):
    """ Get interface ip_address from device

        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object

        Returns:
            None
            interface ip_address ('str')

        Raises:
            None
    """
    log.info("Getting interface address for {interface} on {device}"
        .format(interface=interface, device=device.name))

    cmd = "show ip interface brief"
    try:
        out = device.parse(cmd)
    except SubCommandFailure:
        log.error("Invalid command")
    except Exception as e:
        log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
        return

    address = out["interface"].get(interface, {}).get("ip_address", None)
    if interface not in out["interface"]:
        return
    elif (address == "unassigned" or 
        "ip_address" not in out["interface"][interface]):
        return

    return address

def get_interface_information(device, interface_list):
    """Get interface information from device for a list of interfaces

        Args:
            List['string']: Interfaces to query information on
            device ('obj'): Device object
        Returns:
            List containing Dictionaries for sucesses
    """
    results = {}
    empty_ints = [] 
        
    for interface in interface_list:
        try:
            data = device.parse('show interfaces ' + interface)
        except SchemaEmptyParserError:
            empty_ints.append(interface)
            data = None
        results[interface] = data

    if empty_ints:
        log.error('No interface information found for {}'.format(empty_ints))
    return results

def get_interface_ipv4_address(device, interface):
    """Get the ip address for an interface on target device

        Args:
            interface ('string'): interface to get address for
            device: ('obj'): Device Object
        Returns:
            None
            String with interface ip address
    """

    try:
        data = device.parse('show interfaces ' + interface)
    except SchemaEmptyParserError as e:
        log.error('No interface information found for {}: {}'.format(interface, e))
        return None
    interface = Common.convert_intf_name (interface)
    ip_dict = data[interface].get('ipv4')
    ip = None
    if ip_dict:
        ip = list(ip_dict)[0]
    return ip

def get_ipv6_interface_ip_address(device, interface, link_local=False):
    """ Get interface ip address from device

        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object
            link_local ('bool'): Link local address. Default: False
        Returns:
            None
            ip_address ('str'): If has multiple addresses
                                will return the first one.

        Raises:
            None
    """
    try:
        if '.' in interface and interface.split('.')[1]=='0':
            interface = interface.split('.')[0]
        out=device.parse('show ipv6 interface {interface}'.format(interface=interface))
    except SchemaEmptyParserError as e:
        log.error('No interface information found for {}: {}'.format(interface, e))
        return None
    # Example output
    # {
    #     'GigabitEthernet0/0/0/0': {
    #         'enabled': True,
    #         'oper_status': 'up',
    #         'vrf': 'default',
    #         'int_status': 'up',
    #         'ipv6': {
    #             'incomplete_protocol_adj': '0',
    #             'complete_glean_adj': '0',
    #             'dropped_protocol_req': '0',
    #             'dropped_glean_req': '0',
    #             'nd_router_adv': '1800',
    #             'complete_protocol_adj': '0',
    #             'icmp_unreachables': 'enabled',
    #             'ipv6_link_local': 'fe80::250:56ff:fe8d:8d58',
    #             'incomplete_glean_adj': '0',
    #             'nd_adv_duration': '160-240',
    #             'ipv6_groups': ['ff02::1:ff00:1', 'ff02::1:ff8d:8d58', 'ff02::2', 'ff02::1'],
    #             'nd_adv_retrans_int': '0',
    #             'nd_cache_limit': '1000000000',
    #             'stateless_autoconfig': True,
    #             'icmp_redirects': 'disabled',
    #             'dad_attempts': '1',
    #             'ipv6_mtu': '1514',
    #             'ipv6_mtu_available': '1500',
    #             '2001:112::1/64': {
    #                 'ipv6_subnet': '2001:112::',
    #                 'ipv6_prefix_length': '64',
    #                 'ipv6': '2001:112::1',
    #             },
    #             'nd_dad': 'enabled',
    #             'nd_reachable_time': '0',
    #             'table_id': '0xe0800000',
    #         },
    #         'vrf_id': '0x60000000',
    #         'ipv6_enabled': True,
    #     },
    # }
    # get the interface
    intf = list(out.keys())[0]
    intf = Common.convert_intf_name (intf)
    if link_local:
        return out[intf]['ipv6']['ipv6_link_local']
    
    for sub_key, sub_value in out[intf]['ipv6'].items():
        
        if type(sub_value) == dict:
            sub_value_keys = list(sub_value.keys())

            if 'ipv6' in sub_value_keys:
                return sub_value['ipv6']
    return None    


def get_interfaces_status(device):
    """Get up/down status of all interfaces

    Args:
        device (obj): device object
    """

    try:
        out=device.parse('show ip interface brief')
    except SchemaEmptyParserError as e:
        log.error('No interface information found')
        return None

    # {'interface': {'GigabitEthernet1': {'interface_is_ok': 'YES',
    #           'ip_address': '172.16.1.210',
    #           'method': 'DHCP',
    #           'protocol': 'up',
    #           'status': 'up'},

    return {key:val.get('interface_status') for key, val in out.get('interface', {}).items()}
