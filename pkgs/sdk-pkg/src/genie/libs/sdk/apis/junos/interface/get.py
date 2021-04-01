"""Common get info functions for Interface"""

# Python
import re
import logging
import copy
import ipaddress

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils import Dq
# Pyats
from pyats.utils.objects import find, R

# unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_interface_address_mask_running_config(device, interface,
                                              address_family):
    """ Get interface address and mask from show running-config interface {interface}
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            address_family ('str'): Address family

        Returns:
            (Interface IP address, Interface Mask)

        Raise:
            None
    """
    try:
        output = device.execute('show configuration interfaces {interface}'
                                .format(interface=interface))
    except SubCommandFailure:
        return None, None

    if not output:
        return None, None

    if address_family in ['ipv4', 'inet']:
        # address 192.168.0.1/32
        p1 = re.compile(r'address +(?P<ip>[\d\.]+)/(?P<mask>\d+);')
    elif address_family in ['ipv6', 'inet6']:
        # address 2001:db8:1005:4401::b/128
        p1 = re.compile(r'address +(?P<ip>[\w\:]+)/(?P<mask>\d+);')
    else:
        log.info(
            'Must provide one of the following address families: "ipv4", "ipv6", "inet", "inet6"'
        )
        return None, None

    match = p1.findall(output)
    if match:
        return match[0][0], device.api.int_to_mask(int(match[0][1]))

    return None, None


def get_interface_ip_address(device, interface, address_family,link_local=False,
                             return_all=False):
    """ Get interface ip address from device

        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object
            address_family ('str'): Address family
            link_local ('bool'): Link local address
            return_all ('bool'): return List of values
        Returns:
            None
            ip_address ('str'): If has multiple addresses
                                will return the first one.

        Raises:
            None
    """
    if address_family not in ["ipv4", "ipv6", "inet", "inet6"]:
        log.info('Must provide one of the following address families: '
                 '"ipv4", "ipv6", "inet", "inet6"')
        return

    if address_family == "ipv4":
        address_family = "inet"
    elif address_family == "ipv6":
        address_family = "inet6"

    try:
        out = device.parse(
            'show interfaces terse {interface}'.format(interface=interface))
    except SchemaEmptyParserError:
        return

    # Example dictionary structure:
    #         {
    #             "ge-0/0/0.0": {
    #                 "protocol": {
    #                     "inet": {
    #                         "10.189.5.93/30": {
    #                             "local": "10.189.5.93/30"
    #                         }
    #                     },
    #                     "inet6": {
    #                         "2001:db8:223c:2c16::1/64": {
    #                             "local": "2001:db8:223c:2c16::1/64"
    #                         },
    #                         "fe80::250:56ff:fe8d:c829/64": {
    #                             "local": "fe80::250:56ff:fe8d:c829/64"
    #                         }
    #                     },
    #                 }
    #             }
    #         }

    found = Dq(out).contains(interface).contains(address_family). \
        get_values("local")
    if found:
        if return_all:
            return found
        if link_local:
            return found[1]
        return found[0]
    return None

def get_address_without_netmask(device, interface, address_family,
                             return_all=False, link_local=False):
    """ Get interface ip address without mask

        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object
            address_family ('str'): Address family
            return_all ('bool'): return List of values. Defaults to False
                                 Default to False
            link_local (`bool`): flag to get link-local address for IPv6
        Returns:
            None
            ip_address ('str'): If has multiple addresses
                                will return the first one.

        Raises:
            None
    """
    ip_addr_with_mask = get_interface_ip_address(
                            device=device,
                            interface=interface,
                            address_family=address_family, link_local=link_local)

    if ip_addr_with_mask:
        return ip_addr_with_mask.split('/')[0]

    return None

def get_interface_speed(device, interface, bit_size='gbps'):
    """Get speed of an interface

    Args:
        device (obj): device object
        interface (str): interface name
        bit_size (str): desired return size (gbps/mbps/kbps)
    
    Returns:
        Device speed or None

    Raises:
        None
    """

    try:
        out = device.parse('show interfaces extensive {interface}'.format(
            interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None

    # Example Dictionary
    # "physical-interface": [
    #             {
    #                 "name": "ge-0/0/0",
    #                 "speed": "1000mbps",
    #               }

    speed_matrix = {
        'kbps': {
            'kbps': 1,
            'mbps': 1000,
            'gbps': 1000000,
        },
        'mbps': {
            'kbps': 0.001,
            'mbps': 1,
            'gbps': 1000,
        },
        'gbps': {
            'kbps': .0000001,
            'mbps': 0.001,
            'gbps': 1,
        },
    }

    interfaces_list = Dq(out).get_values('physical-interface')
    for interfaces_dict in interfaces_list:
        speed_ = Dq(interfaces_dict).get_values('speed', 0)
        if not speed_:
            continue

        if 'kbps' in speed_:
            speed_ = int(re.sub(r'[a-zA-Z,]', '',
                                speed_)) / speed_matrix['kbps'][bit_size]
        elif 'mbps' in speed_:
            speed_ = int(re.sub(r'[a-zA-Z,]', '',
                                speed_)) / speed_matrix['mbps'][bit_size]
        else:
            speed_ = int(re.sub(r'[a-zA-Z,]', '',
                                speed_)) / speed_matrix['gbps'][bit_size]
        return speed_


def get_interface_output_error_drops(device, interface):
    """ Get output error drops based on interface name

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            
        Returns:
            output_drops: Output error drops

        Raises:
            None
    """
    try:
        out = device.parse('show interfaces extensive {interface}'.format(
            interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None

    output_drops = out.q.get_values('output-drops', 0)
    if not output_drops:
        return None
    return output_drops

def get_interface_statistics_output_error_drops(device, interface):
    """ Get output error drops based on interface statistics

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            
        Returns:
            output_drops: Output error drops

        Raises:
            None
    """
    try:
        out = device.parse('show interfaces statistics {interface}'.format(
            interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None

    output_drops = out.q.get_values('output-error-count', 0)
    if not output_drops:
        return None
    return output_drops

def get_interface_queue_tail_dropped_packets(device, interface):
    """ Get tail-dropped packets based on interfaces queue

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            
        Returns:
            tail_drop_packets: Output error drops

        Raises:
            None
    """
    try:
        out = device.parse('show interfaces queue {interface}'.format(
            interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None

    tail_drop_packets = out.q.get_values('queue-counters-tail-drop-packets')
    if not tail_drop_packets:
        return None
    return tail_drop_packets

def get_interface_queue_rl_dropped_packets(device, interface):
    """ Get rl-dropped packets based on interfaces queue

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            
        Returns:
            rl_drop_packets: Output error drops

        Raises:
            None
    """
    try:
        out = device.parse('show interfaces queue {interface}'.format(
            interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None

    rl_drop_packets = out.q.get_values('queue-counters-rl-drop-packets')
    if not rl_drop_packets:
        return None
    return rl_drop_packets

def get_interface_queue_red_dropped_packets(device, interface):
    """ Get red-dropped packets based on interfaces queue

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            
        Returns:
            red_drop_packets: Output error drops

        Raises:
            None
    """
    try:
        out = device.parse('show interfaces queue {interface}'.format(
            interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None

    red_drop_packets = out.q.get_values('queue-counters-red-packets')
    if not red_drop_packets:
        return None
    return red_drop_packets


def get_interface_queue_counters_dropped(device,
                                         interface,
                                         expected_queue_number,
                                         extensive=False):
    """ Get queue counters dropped based on interfaces queue

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_queue_number ('str'): Queue number to check
            extensive ('str'): Flag to check extensive in command
            
        Returns:
            total_drop_packets: Output error drops

        Raises:
            None
    """
    try:
        if extensive:
            out = device.parse('show interfaces extensive {interface}'.format(
                interface=interface.split('.')[0]))
        else:
            out = device.parse('show interfaces {interface}'.format(
                interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None

    total_drop_packets = out.q.get_values('queue-counters-total-drop-packets',
                                          int(expected_queue_number))
    if not total_drop_packets:
        return None
    return total_drop_packets


def get_interface_logical_output_bps(device,
                                     logical_interface,
                                     interface=None,
                                     extensive=False,
                                     output_dict=None):
    """Get logical output bps of a logical interface

    Args:
        device ('obj'): device object
        logical_interface ('str'): Logical interface to check output bps
        interface ('str'): interface name to pass in show command
        extensive ('bool'): Use extensive in show command
        output_dict ('dict'): Pass if dictionary already exist
    
    Returns:
        Device speed or None

    Raises:
        None
    """
    out = None
    try:
        if not output_dict:
            try:
                if interface:
                    cmd = 'show interfaces {interface}'.format(
                        interface=interface)
                else:
                    cmd = 'show interfaces'
                if extensive:
                    cmd = '{cmd} extensive'.format(cmd=cmd)
                out = device.parse(cmd)
            except SchemaEmptyParserError:
                return None
        else:
            out = output_dict

    except SchemaEmptyParserError:
        return None
    result = True

    # Get first interface inorder to compare output-bps with other interfaces
    physical_intf_check = out.q.contains(
        '{interface}|.*output-bps.*'.format(interface=logical_interface),
        regex=True)

    # To handle list within list
    logical_interface_check = Dq(physical_intf_check.reconstruct())

    logical_intf_list = logical_interface_check.contains(
        'name|output-bps', regex=True).get_values('logical-interface')

    for l_i_dict in logical_intf_list:
        name = l_i_dict.get('name', None)
        if not name or name != logical_interface:
            continue

        transit_traffic_statistic = l_i_dict.get('transit-traffic-statistics',
                                                 0)

        if not transit_traffic_statistic:
            return None

        output_bps = transit_traffic_statistic.get('output-bps', 0)
        if not output_bps:
            return None

        return output_bps

    return None


def get_interface_queue_counters_trans_packets(device,
                                               interface,
                                               expected_queue_number,
                                               extensive=False):
    """ Get queue counters transmitter based on interfaces queue

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_queue_number ('str'): Queue number to check
            extensive ('str'): Flag to check extensive in command
            
        Returns:
            total_drop_packets: Output error drops

        Raises:
            None
    """
    try:
        if extensive:
            out = device.parse('show interfaces extensive {interface}'.format(
                interface=interface.split('.')[0]))
        else:
            out = device.parse('show interfaces queue {interface}'.format(
                interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None
    # Dcitonary:
    # 'queue': [{'queue-counters-queued-packets': '0',
    #             'queue-counters-total-drop-packets': '0',
    #             'queue-counters-trans-packets': '0',
    #             'queue-number': '0'}]
    transmitted_drop_packets = out.q.get_values('queue-counters-trans-packets',
                                                int(expected_queue_number))
    if not transmitted_drop_packets:
        return None
    return transmitted_drop_packets


def get_interface_queue_counters_queued_packets(device,
                                                interface,
                                                expected_queue_number,
                                                extensive=False):
    """ Get queued packets based on queue number

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_queue_number ('str'): Queue number to check
            extensive ('str'): Flag to check extensive in command
            
        Returns:
            total_drop_packets: Output error drops

        Raises:
            None
    """
    try:
        if extensive:
            out = device.parse('show interfaces extensive {interface}'.format(
                interface=interface.split('.')[0]))
        else:
            out = device.parse('show interfaces {interface}'.format(
                interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None
    # Dcitonary:
    # 'queue': [{'queue-counters-queued-packets': '0',
    #             'queue-counters-total-drop-packets': '0',
    #             'queue-counters-trans-packets': '0',
    #             'queue-number': '0'}]
    queue_counters_queued_packets = out.q.get_values(
        'queue-counters-queued-packets', int(expected_queue_number))
    if not queue_counters_queued_packets:
        return None
    return queue_counters_queued_packets

def get_interface_traffic_output_pps(device: object, interface: str) -> str:
    """Get interface output pps

    Args:
        device (object): Device object
        interface (str): Interface to check

    Returns:
        str: Interface pps
    """

    try:
        out = device.parse('show interfaces {interface} extensive'.format(
            interface=interface))
    except SchemaEmptyParserError as e:
        return None

    # Example dict
    #     "interface-information": {
    #         "physical-interface": [
    #             {
    #                 "traffic-statistics": {
    #                     "output-pps": str

    phy_ = out.q.get_values('physical-interface', 0)
    return phy_.get('traffic-statistics').get('output-pps')

def get_interface_traffic_input_pps(device: object, interface: str) -> str:
    """Get interface input pps

    Args:
        device (object): Device object
        interface (str): Interface to check

    Returns:
        str: Interface pps
    """

    try:
        out = device.parse('show interfaces {interface} extensive'.format(
            interface=interface))
    except SchemaEmptyParserError as e:
        return None

    # Example dict
    #     "interface-information": {
    #         "physical-interface": [
    #             {
    #                 "traffic-statistics": {
    #                     "input-pps": str

    phy_ = out.q.get_values('physical-interface', 0)
    return Dq(phy_).get_values('input-pps',0)


def get_interface_queue_counters_transmitted_byte_rate(device, interface,
                                                       expected_queue_number):
    """ Get queue counters transmitted byte rate based on interfaces queue

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            expected_queue_number ('str'): Queue number to check
            
        Returns:
            total_drop_packets: Output error drops

        Raises:
            None
    """
    try:
        out = device.parse('show interfaces queue {interface}'.format(
            interface=interface.split('.')[0]))
    except SchemaEmptyParserError as e:
        return None

    transmitted_byte_rate = out.q.get_values('queue-counters-trans-bytes-rate',
                                             int(expected_queue_number))
    if not transmitted_byte_rate:
        return None
    return transmitted_byte_rate

def get_interface_network_address(device, interface, address_family='ipv4',link_local=False,
                             return_all=False):
    """ Get interface network address from device
        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object
            address_family ('str'): Address family. Default to 'ipv4'
            link_local ('bool'): Link local address. Default to False
            return_all ('bool'): return List of values. Default to False
        Returns:
            None
            network_address ('str'): If has multiple network addresses
                                     will return the first one.
        Raises:
            None
    """
    if address_family not in ["ipv4", "ipv6", "inet", "inet6"]:
        log.info('Must provide one of the following address families: '
                 '"ipv4", "ipv6", "inet", "inet6"')
        return

    if address_family == "ipv4":
        address_family = "inet"
    elif address_family == "ipv6":
        address_family = "inet6"

    ip_address_list = device.api.get_interface_ip_address(interface=interface, address_family=address_family, return_all=True)

    found = []

    if ip_address_list:
        for ip in ip_address_list:
            if address_family == "inet":
                found.append(str(ipaddress.IPv4Interface(ip).network))
            elif address_family == "inet6":
                found.append(str(ipaddress.IPv6Interface(ip).network))

        if found:
            if return_all:
                return found
            if link_local and address_family == "ipv6":
                link_local_found = []
                for item in found:
                    if ipaddress.IPv6Address(item.split('/')[0]).is_link_local:
                        link_local_found.append(item)
                return link_local_found
            return found[0]
    return None

def get_interfaces_description(device, interface=None):
    """Get the description of given interface via 'show interfaces descriptions {interface}'
        Args:
            device ('obj'): Device object
            interface('str'): Interface name, default: None

        Returns:
            Boolean

        Raises:
            None
    """

    try:
        out = device.parse('show interfaces descriptions {interface}'.format(
            interface=interface))
    except SchemaEmptyParserError as e:
        return None

    # Sample output
    # {
    # "interface-information": {
    #     "physical-interface": [
    #         {
    #             "admin-status": "up",
    #             "description": "none/100G/in/hktGCS002_ge-0/0/0", <------------
    #             "name": "ge-0/0/0", <---- Given interface
    #             "oper-status": "up",
    #         },
    # ...

    physical_interface_list = out.q.get_values('physical-interface', None)

    for intf in physical_interface_list:
        if intf['name'] == interface:
            return intf['description']

    return None


def get_interface_traffic_stats(device, interface, stat_name, extensive=True):
    """Get the traffic stats of given interface via 'show interfaces {interface} extensive'
        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            stat_name (`str`): stat name under `traffic-statistics`
            extensive (`bool`): flag to use `show interface {interface} extensive`

        Returns:
            int (value of stat_name)

        Raises:
            None
    """

    try:
        if extensive:
            parsed_output = device.parse(
                'show interfaces {interface} extensive'.format(
                    interface=interface))
        else:
            parsed_output = device.parse(
                'show interfaces {interface}'.format(
                    interface=interface))
    except SchemaEmptyParserError as e:
        return None

    physical_interface = parsed_output.q.get_values('physical-interface', 0)
    if stat_name in physical_interface['traffic-statistics']:
        return int(physical_interface['traffic-statistics'][stat_name])

    log.warn(
        "given stat_name {stat_name} is not correct. traffic-statistics: {traffic_stats}"
        .format(stat_name=stat_name,
                traffic_stats=physical_interface['traffic-statistics']))
    return None


def get_interface_ipv4_address(device, interface):
    """Get the ip address for an interface on target device

        Args:
            interface ('string'): interface to get address for
            device: ('obj'): Device Object
        Returns:
            None
            String with interface ip address
    """

    return get_interface_ip_address(device, interface, 'ipv4')



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
    return get_interface_ip_address(device, interface, 'ipv6', link_local=link_local)
    
def get_diagnostics_optics_stats(device, interface, stat_name, lane_number=None):
    """Get the traffic stats of given interface via show interfaces diagnostics optics {interface}
        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            stat_name ('str'): stat name under `traffic-statistics`
            lane_number ('int'): lane number

        Returns:
            str (value of stat_name)

        Raises:
            None
    """
    try:
        parsed_output = device.parse(
            'show interfaces diagnostics optics {interface}'.format(
                interface=interface))
    except SchemaEmptyParserError as e:
        return None

    # Sample output
    # {
    # "interface-information": {
    #     "physical-interface": [
    #         {
    #             "name": "xe-0/1/7",
    #             "optics-diagnostics": {
    #                 "laser-bias-current": "37.682 mA",
    #                 "laser-output-power": "0.6560 mW / -1.83 dBm",
    #                 "module-temperature": "36 degrees C / 97 degrees F",
    #                 "module-voltage": "3.2680 V",
    #                 (snip)
    #             }
    #             "lanes": [
    #                 {
    #                     "lane-number": "0",
    #                     "laser-bias-current": "132.255 mA",
    #                     "laser-output-power": "1.348 mW / 1.30 dBm",
    #                     (snip)
    #                 }
    #             ]
    #         }
    #     ]
    # }}


    physical_interface = parsed_output.q.get_values('physical-interface', 0)

    if type(lane_number) == int:
        if lane_number>=0:
            lanes_list = physical_interface["optics-diagnostics"]["lanes"]
            return lanes_list[lane_number][stat_name]

    if stat_name in physical_interface['optics-diagnostics']:
        return physical_interface['optics-diagnostics'][stat_name]

    log.warn(
        "given stat_name {stat_name} is not correct. optics-diagnostics: {optics_diagnostics}"
        .format(stat_name=stat_name,
                optics_diagnostics=physical_interface['optics-diagnostics']))
    return None
def get_interfaces_terse_columns(device, expected_columns):
    """Get the description of given interface via 'show interfaces descriptions {interface}'
        Args:
            device ('obj'): Device object
            expected_columns('str'): Expected columns based on parser table
                Example:  columns: ['interface', 'admin_state', 'enabled', 'link_state', 'oper_status']
        Returns:
            Boolean
        Raises:
            None
    """

    try:
        out = device.parse('show interfaces terse')
    except SchemaEmptyParserError as e:
        return None

    # {
    # "ge-0/0/0": {
    #     "admin_state": "up",
    #     "enabled": True,
    #     "link_state": "up",
    #     "oper_status": "up"
    # },

    columns = '|'.join(expected_columns)
    interface_dict = out.q.contains('{}'.format(columns), regex=True).reconstruct()
    rows_ = []
    for k,v in interface_dict.items():
        rows_.append(tuple([k] + list(v.values())))
    return rows_ or None


def get_interface_field(device, interface, field, output=None):
    """ Get specific field value from show interfaces

        Args:
            device (`obj`): Device object
            interface (`str`): interface name
            field (`str`): field name where want to get value
            output (`str`): output of show interfaces {interface}
                            Default to None
        Returns:
            value (`str`): ifindex number
    """

    try:
        out = device.parse('show interfaces {int}'.format(int=interface),
                           output=output)
    except SchemaEmptyParserError:
        return None

    # example of out
    # {
    #   "interface-information": {
    #     "physical-interface": [
    #       {
    #         "logical-interface": [
    #           {
    #             "address-family": [],
    #             "encapsulation": "ENET2",
    #             "if-config-flags": {
    #               "iff-snmp-traps": true,
    #               "iff-up": true,
    #               "internal-flags": "0x4004000"
    #             },
    #             "local-index": "333",
    #             "name": "ge-0/0/1.0",
    #             "snmp-index": "540",
    #             "traffic-statistics": {
    #               "input-packets": "189",
    #               "output-packets": "195"
    #             }
    #           }
    #         ],
    #         "name": "ge-0/0/1"
    #       }
    #     ]
    #   }
    # }
    field_value = out.q.get_values(field, 0)
    if field_value:
        return field_value
    else:
        return None


def get_interface_snmp_index(device,
                             interface):
    """ Get local index number

        Args:
            device ('obj'): Device object
            interface('str'): Interface name
            
        Returns:
            total_drop_packets: Output error drops
        Raises:
            None
    """
    try:
        out = device.parse('show interfaces {interface}'.format(
            interface=interface))
    except SchemaEmptyParserError as e:
        return None

    # Sample output
    #"logical-interface": [
    #                {
    #                    "address-family": [],
    #                    "encapsulation": "ENET2",
    #                    "if-config-flags": {
    #                        "iff-snmp-traps": True,
    #                        "iff-up": True,
    #                        "internal-flags": "0x4004000"
    #                    },
    #                    "local-index": "333",
    #                    "name": "ge-0/0/0.0",
    #                    "snmp-index": "606",
    #                    "traffic-statistics": {
    #                        "input-packets": "133657033",
    #                        "output-packets": "129243982"
    #                    }
    #                }
    #            ]

    return(out.q.get_values("snmp-index",0))
