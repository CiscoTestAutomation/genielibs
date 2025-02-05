"""Common get info functions for routing"""

# Python
import logging

# pyATS
from pyats.utils.objects import find, R
import re

# Genie
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError
import genie.libs.sdk.apis.iosxe.routing.util as util

log = logging.getLogger(__name__)


def get_routing_ospf_routes(device):
    """ Retrieve all ospf routes - show ip route

        Args:
            device ('obj'): Device object
        Returns:
            routes ('list'): List of ospf routes
    """
    log.info("Getting all ospf routes")
    protocol_codes = 'O'
    return get_routes(device, protocol_codes)


def get_routes(device, protocol_codes=None, route=None, vrf='default'):
    """ Retrieve all routes in specific protocol - show ip route

        Args:
            device ('obj'): Device object
            protocol_codes ('str'): Protocol codes
                If not provided, it will get all protocal routes
            route ('str'): destination route
            vrf ('str): VRF name. default to 'default'
        Returns:
            routes ('list'): List of routes
    """
    routes = []
    af = 'ipv6' if route and ':' in route else 'ip'
    cmd = f'show {af} route'
    if vrf != 'default':
        cmd += f' vrf {vrf}'
    if route:
        cmd += f' {route}'

    try:
        out = device.parse(cmd)
    except Exception as e:
        log.error(f"Failed to parse '{cmd}':\n{e}")
        return routes

    if route:
        return out.q.get_values('entry')
    if protocol_codes:
        return out.q.contains_key_value(
            'source_protocol_codes', protocol_codes).get_values('routes')
    else:
        return out.q.get_values('routes')


def get_routing_outgoing_interface(device,
                                   ip_address,
                                   vrf=None,
                                   address_family=None):
    """ Execute 'show ip cef <address>' and retrieve the outgoing interface

        Args:
            device (`obj`): Device object
            ip_address ('str'): ip_address
            vrf ('str'): vrf to search under
            address_family ('str'): address_family to search under

        Returns:
            ('list'): [interface name, ip_address]

        Raises:
            SchemaEmptyParserError

    """

    log.info("Get the outgoing interface ('show ip cef <ip>')")

    outgoing_interface = None
    new_ip = None

    try:
        out = device.parse("show ip cef {ip}".format(ip=ip_address))
    except SchemaEmptyParserError:
        return []

    vrf = vrf or "default"
    address_family = address_family or "ipv4"

    for prefix, p_data in out["vrf"][vrf]["address_family"][address_family][
            "prefix"].items():
        for next_hop, nh_data in p_data.get("nexthop", {}).items():
            for key in nh_data.get("outgoing_interface", {}):
                outgoing_interface = key
                new_ip = next_hop
                break
        continue

    return [outgoing_interface, new_ip]


def get_routing_route_count(device, vrf=None):
    """ Get route count for all vrfs

        Args:
            device(`str`): Device str
            vrf ('str'): VRF name

        Returns:
            int: route count

        Raises:
            SchemaEmptyParserError
    """

    commands = ["show ip route vrf {} summary", "show ip route summary"]

    cmd = commands[0].format(vrf) if vrf else commands[1]
    try:
        output = device.parse(cmd)
    except SchemaEmptyParserError:
        raise SchemaEmptyParserError("Command '{}' has "
                                     "not returned any results".format(cmd))
    if not vrf:
        vrf = "default"

    return output.get("vrf", {}).get(vrf, {}).\
            get("total_route_source", {}).get("subnets")


def get_routing_route_count_all_vrf(device):
    """ Get route count for every VRF

        Args:
            device ('obj'): Device object

        Returns:
            Integer: Route count

        Raises:
            SchemaEmptyParserError
    """
    log.info("Getting route count for all vrf")
    try:
        out = device.parse("show vrf")
    except SchemaEmptyParserError as e:
        raise SchemaEmptyParserError("Could not find any VRF")

    route_count = 0

    # Gets route count when VRF is 'default'
    try:
        route_count += get_routing_route_count(device=device)
    except SchemaEmptyParserError as e:
        pass

    for vrf in out["vrf"]:
        try:
            route_count += get_routing_route_count(device=device, vrf=vrf)
        except SchemaEmptyParserError as e:
            pass

    log.info("Route count for all vrf is {}".format(route_count))
    return route_count


def get_routing_routes(device, vrf, address_family):
    """Execute 'show ip route vrf <vrf>' and retrieve the routes

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name or None
            address_family (`str`): Address family name

        Returns:
            Dictionary: received routes

        Raises:
            SchemaEmptyParserError
            KeyError

    """
    # only accept ipv4 address family
    address_family = address_family.split()[0]
    try:
        if vrf:
            command = "show ip route vrf {}".format(vrf)
        else:
            command = "show ip route"
        out = device.parse(command)
    except SchemaEmptyParserError:
        log.error(
            "Parser did not return any routes for vrf {vrf}".format(vrf=vrf))
        return None
    try:
        if not vrf:
            vrf = "default"
        routes_received = out["vrf"][vrf]["address_family"][address_family][
            "routes"]
    except KeyError as e:
        log.error("Key issue with exception : {}".format(str(e)))
        return None

    return routes_received


def get_routing_repair_path_information(device, route):
    """ Get 'repair path' information under route

        Args:
            device ('obj'): Device object
            route ('str'): Route address
        Returns:
            tuple : (
                next_hop ('str'): Next hop ip
                outgoing_interface ('str'): Outgoing interface name
            )            
        Raises:
            None
    """

    try:
        output = device.parse("show ip route {route}".format(route=route))
    except SchemaEmptyParserError:
        log.info("Could not find any information about repair path")
        return None, None

    for rt in output["entry"]:
        for path_index in output["entry"][rt]["paths"]:
            repair_path = output["entry"][rt]["paths"][path_index].get(
                "repair_path", {})
            if repair_path:
                log.info(
                    "Found repair path {path[repair_path]} via {path[via]}".
                    format(path=repair_path))
                next_hop = repair_path["repair_path"]
                outgoing_interface = repair_path["via"]

                return next_hop, outgoing_interface

    log.info("Could not find any information about repair path")
    return None, None


def get_routing_mpls_label(device, prefix, vrf='', output=None):
    ''' Get registered MPLS label to prefix 
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            vrf (`vrf`): VRF name
            output ('dict'): Optional. Parsed output of command 'show ip route {prefix}'
        Returns:
            int: registered MPLS label
        Raises:
            None

    '''

    log.info('Getting registered MPLS label to prefix {prefix}'.format(
        prefix=prefix))

    if not output:
        try:
            if vrf:
                output = device.parse(
                    'show ip route vrf {vrf} {prefix}'.format(vrf=vrf,
                                                              prefix=prefix))
            else:
                output = device.parse(
                    'show ip route {prefix}'.format(prefix=prefix))
        except SchemaEmptyParserError:
            log.info('Could not find any MPLS label to prefix '
                     'address {prefix}'.format(prefix=prefix))

    for entry in output['entry']:
        for prefix in entry:
            for path in output['entry'][entry].get('paths', {}):
                label = output['entry'][entry]['paths'][path].get(
                    'mpls_label', None)
                if label:
                    log.info('Found MPLS label {label}'.format(label=label))
                    return int(label)

    log.info('Could not find any MPLS label to prefix '
             'address {prefix}'.format(prefix=prefix))

    return None


def get_routing_vrf_entries(device, prefix, vrf=None):
    ''' Get entry of routes from
        'show ip route vrf {vrf} {prefix}'/'show ip route {prefix}'
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            vrf (`str`, optional): VRF name, default None
        Returns:
            list: entries of ip
            None
        Raises:
            None

    '''
    if vrf:
        command = "show ip route vrf {vrf} {prefix}".format(vrf=vrf,
                                                            prefix=prefix)
    else:
        command = "show ip route {prefix}".format(prefix=prefix)

    try:
        output = device.parse(command)
    except SchemaEmptyParserError:
        log.error(
            'Routing table is empty for route {prefix}'.format(prefix=prefix))
        return None

    entries = []
    for entry in output['entry']:
        received_entry = output['entry'][entry].get('ip', '')
        entries.append(received_entry)

    return entries


def get_routing_ipv6_routes(device, vrf=None):
    """Execute 'show ipv6 route vrf <vrf>' and retrieve the routes

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF name or None

        Returns:
            Dictionary: received routes
            {}: When exception is hit

        Raises:
            SchemaEmptyParserError
            KeyError

    """
    try:
        if vrf:
            command = "show ipv6 route vrf {}".format(vrf)
        else:
            command = "show ipv6 route"
        out = device.parse(command)
    except SchemaEmptyParserError:
        log.error(
            "Parser did not return any routes for vrf {vrf}".format(vrf=vrf))
        return {}
    try:
        if not vrf:
            vrf = "default"
        routes_received = out["vrf"][vrf]["address_family"]['ipv6'][
            "routes"]
    except KeyError as e:
        log.error("Key issue with exception : {}".format(str(e)))
        return {}

    return routes_received

def get_routing_route_source_protocol(device, route, output=None):
    """
    Gets the source protocol of route from
    'show ip route' parsed dict output.
    Args:
        device (`obj`): Device object
        route (`str`): ipv4 route address
        output (`dict`): already parsed show ip route output
    Raises:
        SchemaEmptyParserError
    Returns: 
        None if route does not exist.
    """
    try:
        if device:
            output = device.parse('show ip route')
        elif device is None and output is None:
            log.error("Please input a 'show ip route' dict output or a device")
            return None
    except SchemaEmptyParserError:
        log.info("No output from parser for show ip route\n")
        raise SchemaEmptyParserError

    try:
        route_dict = output['vrf']['default']['address_family']['ipv4']['routes']
        for masked_route in route_dict:
            if route in masked_route:
                return route_dict[masked_route]['source_protocol_codes']

        return None

    except Exception as e:
        log.error("An exception has occurred.\n{}".format(e))
        return None

def get_next_hops(device, route, output=None, vrf=None):
    """
    Gets the next hops from 'show [ip|ipv6] route' parsed output.

    Args:
        device (, optional): Device used to run commands
        route ('str'): Route to check for next hops
        output (dict, optional): 'show [ip|ipv6] route' parsed dict output
        vrf ('str): VRF name

    Returns tuple of next hop addresses; returns None if dne
    """
    try:
        if ':' in route:
            af = 'ipv6'
            af_parsed = 'ipv6'
        else:
            af = 'ip'
            af_parsed = 'ipv4'

        cmd = f'show {af} route'
        if vrf:
            cmd += f' vrf {vrf}'

        if output is None:
            output = device.parse(cmd)
        elif device is None and output is None:
            log.error("Please input a 'show [ip|ipv6] route' dict output or a device")
            return None

        if not vrf:
            vrf = 'default'

        route_next_hops = tuple()
        route_dict = output['vrf'][vrf]['address_family'][af_parsed]['routes']
        for masked_route in route_dict:
            if route in masked_route:
                next_hop_list = route_dict[masked_route]['next_hop']['next_hop_list']
                for index in next_hop_list:
                    next_hop = next_hop_list[index]['next_hop']
                    route_next_hops += (next_hop, )

        return None if not route_next_hops else route_next_hops

    except Exception as e:
        log.error("An exception has occurred.\n{}".format(e))
        return None


def get_next_hops_with_vrf(device, route, output=None, vrf='default'):
    """
    Gets the next hops from 'show [ip|ipv6] route' parsed output.

    Args:
        device (, optional): Device used to run commands
        route ('str'): Route to check for next hops
        output ('dict', optional): 'show [ip|ipv6] route' parsed dict output
        vrf ('str'): VRF name. Default to 'default'

    Returns tuple of next hop addresses with vrf and interface; returns empty tuple if no nexthops
    [['FC01:101:8:E007::', 'default', None, 'B']]
    """
    try:
        if ':' in route:
            af = 'ipv6'
            af_parsed = 'ipv6'
        else:
            af = 'ip'
            af_parsed = 'ipv4'

        cmd = f'show {af} route'
        if vrf != 'default':
            cmd += f' vrf {vrf}'

        if output is None:
            output = device.parse(cmd)
        elif device is None:
            log.error(
                "Please input a 'show [ip|ipv6] route' dict output or a device"
            )
            return None

        if not vrf:
            vrf = 'default'

        route_next_hops = []
        route_dict = output['vrf'][vrf]['address_family'][af_parsed]['routes']
        for masked_route in route_dict:
            if route in masked_route:
                next_hop_list = route_dict[masked_route]['next_hop'][
                    'next_hop_list']
                source_protocol_codes = route_dict[masked_route]['source_protocol_codes']
                for index in next_hop_list:
                    if 'vrf' in next_hop_list[index]:
                        vrf = next_hop_list[index]['vrf'].split(':')[0]
                    else:
                        vrf = 'default'
                    if 'next_hop' in next_hop_list[index]:
                        next_hop = next_hop_list[index]['next_hop']
                    else:
                        if 'binding_label' in next_hop_list[index]:
                            binding_label = next_hop_list[index]['binding_label']
                            out = device.parse(f'show ip cef label-table {binding_label} internal')
                            next_hop = out.q.get_values('outgoing_address')
                            out_intf = out.q.get_values('outgoing_interface')
                            for nh, oi in list(set(zip(next_hop, out_intf))):
                                route_next_hops.append([nh, vrf, oi, source_protocol_codes])
                            continue
                        else:
                            raise Exception('No next hop or binding label found')
                    if 'outgoing_interface' in next_hop_list[index]:
                        out_intf = next_hop_list[index]['outgoing_interface']
                    else:
                        out_intf = None
                    route_next_hops.append([next_hop, vrf, out_intf, source_protocol_codes])

        return route_next_hops or []

    except Exception as e:
        log.exception(f"An exception has occurred.\n{e}")
        return None

def get_outgoing_interface_with_vrf(device, route, vrf='default'):
    """
    Gets the outgoing interfaces based on destination route

    Args:
        device (, optional): Device used to run commands
        route ('str'): Route to find out outgoing interafces
        vrf ('str'): VRF name. Default to 'default'

    Returns list of outgoing interfaces with source_protocol_codes
    ex.) [['FE80::A8BB:CCFF:FE02:A04', 'default', 'Ethernet4/0', 'I2']]
    """

    interfaces = []
    def _get_outgoing_interface(route, vrf):
        prefix = device.api.get_routes(route=route, vrf=vrf)
        return device.api.get_next_hops_with_vrf(route=prefix[0], vrf=vrf)

    # recursively loop until outgoing interface is found
    while not interfaces:
        nexthops = _get_outgoing_interface(route, vrf)
        if nexthops:
            for each_nh in nexthops:
                if each_nh[2] is not None:
                    # append outgoing interface
                    interfaces.append(each_nh)
                else:
                    # prevent recursive endless loop
                    if route == each_nh[0] and vrf == each_nh[1]:
                        log.error('Something went wrong.')
                        return []
                    else:
                        route = each_nh[0]
                        vrf = each_nh[1]

    return interfaces


def get_ipv6_routes(device):
    """
        Get routes from 'show ipv6 route' on a device

        Args:
            device(): Device used to run commands
        
        Returns:
            Routes: List of routes
    """

    try:
        output = device.parse('show ipv6 route')
    except Exception as e:
        log.error("An exception occured.\n {}".format(e))
        return None

    routes = list(output['vrf']['default']['address_family']['ipv6']['routes'])
    return routes

def get_ipv6_intf_valid_ip_addresses(device, interface):
    """ Get interface ip addresses from device that are 'valid'
        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object
        Returns:
            None
            ip_address ('list'): A list of valid ip addresses
        Raises:
            None
    """

    try:
        output = device.parse('show ipv6 interface {}'.format(interface))
    except Exception as e:
        log.error("No interface information found on {}".format(interface))
        log.error("Exception occured\n {}".format(e))
        return None

    ipv6_addr = [val for val in output[interface]['ipv6'].values() if type(val) == dict]

    return [ip.get('ip') for ip in ipv6_addr if ip.get('ip') is not None and ip.get('status') == 'valid']

def get_ipv6_linklocal_addr_from_ipv4(device, ipv4_intf, isatap=False):
    """
    Generates ipv6 linklocal address from ipv4 address.

    Args:
        ipv4_addr ('str'): Address used to create linklocal address
        isatap ('bool'): Whether linklocal address is ISATAP or not

    Returns ipv6 linklocal address string.
    """
    ipv4_addr = device.api.get_interface_ip_address(ipv4_intf)
    if not ipv4_addr:
        log.error("Error: ipv4 address from interface {} is {}".format(ipv4_intf, ipv4_addr))
        return None

    ll_addr = ''
    # Parse each octet, convert to hexadecimal and then pad with a 0
    reg = re.compile(r'([\d]+)\.([\d]+)\.([\d]+)\.([\d]+)')
    m = reg.match(ipv4_addr)
    log.info(m)
    if not m:
        # If no match detected, exit function
        log.error("Input ipv4 address does not match expected format.")
        return None
    groups = m.groups()
    octets = []
    for val in groups:
        hex_val = hex(int(val))[2:].zfill(2)
        octets.append(hex_val)
        log.info("hex value: {}".format(hex_val))
    log.info("octet list: {}".format(octets))
    # Place the hex numbers in a string in the following manner:
    #   - <first><second>:<third><fourth>
    # and concatenate with 'FE80::'
    pair1 = (octets[0] + octets[1]).lstrip('0')
    pair2 = (octets[2] + octets[3]).lstrip('0')

    ll_addr = 'FE80::'
    if isatap:
        ll_addr += '5EFE:'
    ll_addr = ('{}{}:{}'.format(ll_addr, pair1, pair2)).upper()

    return util.ipv6_shorten_address(ll_addr)

def get_ipv6_intf_tentative_address(device, interface):
    """ Get interface ip addresses from device that are 'tentative'
        Args:
            interface('str'): Interface to get address
            device ('obj'): Device object
        Returns:
            None
            ip_address ('list'): A list of tentative ip addresses
        Raises:
            None
    """

    try:
        # output = device.parse('show ipv6 interface {}'.format(interface))
        output = device.execute('show ipv6 interface {}'.format(interface))
    except Exception as e:
        log.error("No interface information found on {}".format(interface))
        log.error("Exception occured\n {}".format(e))
        return None



    # device.parser implementation
    # ipv6_addr = [val for val in output[interface]['ipv6'].values() if type(val) == dict]
    # addresses = [ip.get('ip') for ip in ipv6_addr if ip.get('ip') is not None and ip.get('status') == 'tentative']

    # device.execute implementation
    rgx = re.compile(r"\d.*\[.*\/?TEN\]")
    addrs = re.findall(rgx, output)
    addrs = [addr.split(',')[0] for addr in addrs]


    return addrs

def get_ipv6_local_routes(device):
    """
        Gets installed local routes from "show ipv6 route" on a device

        Args:
            device(): Device used to run commands

        Returns:
            Routes: list of routes
    """

    try:
        output = device.parse('show ipv6 route')
    except Exception as e:
        log.error("An exception occured.\n {}".format(e))
        return None

    output = output['vrf']['default']['address_family']['ipv6']['routes']

    routes = [addr for addr, val in output.items() if val.get('source_protocol_codes') == 'L']

    return routes

def get_ipv6_connected_routes(device):
    """
        Gets installed local routes from "show ipv6 route" on a device

        Args:
            device(): Device used to run commands

        Returns:
            Routes: list of routes
    """

    try:
        output = device.parse('show ipv6 route')
    except Exception as e:
        log.error("An exception occured.\n {}".format(e))
        return None

    output = output['vrf']['default']['address_family']['ipv6']['routes']

    routes = [addr for addr, val in output.items() if val.get('source_protocol_codes') == 'C']

    return routes

def get_ipv6_static_routes(device):
    """
        Gets installed static routes from "show ipv6 route" on a device

        Args:
            device(): Device used to run commands

        Returns:
            Routes: list of routes
    """

    try:
        output = device.parse('show ipv6 route')
    except Exception as e:
        log.error("An exception occured.\n {}".format(e))
        return None

    output = output['vrf']['default']['address_family']['ipv6']['routes']

    routes = [addr for addr, val in output.items() if val.get('source_protocol_codes') == 'S']

    return routes

def get_ipv6_intf_autocfg_address(device,interface ):
    """ Gets auto configured IPv6 addresses from device
        Args:
            device ('obj'): Device object
            interface('str'): Interface to get address
        Returns:
            None
            ip_address ('list'): A list of valid ip addresses with its subnet (i.e. 2001::/64)
        Raises:
            None
    """


    try:
        output = device.parse('show ipv6 interface {}'.format(interface))
    except Exception as e:
        log.error("No interface information found on {}".format(interface))
        log.error("An Exception occured:\n {}".format(e))
        return None

    ipv6_addr = [val for val in output[interface]['ipv6'].values() if type(val) == dict]

    auto_cfg_addr = ["{}/{}".format(ip.get('ip'), ip.get("prefix_length")) for ip in ipv6_addr if ip.get('autoconf')]

    return auto_cfg_addr

def get_RIPng_routes(device):
    """
        Gets installed RIPng routes from "show ipv6 route" on a device

        Args:
            device(): Device used to run commands

        Returns:
            Routes: list of routes
    """

    try:
        output = device.parse('show ipv6 route')
    except Exception as e:
        log.error("An exception occured.\n {}".format(e))
        return None

    output = output['vrf']['default']['address_family']['ipv6']['routes']

    routes = [addr for addr, val in output.items() if val.get('source_protocol_codes') == 'R']

    return routes

def get_route_metric(device):
    """
        Gets the ipv6 routes and its corresponding metric of the device via "show ipv6 route"

        Args:
            device: Device used to run commands
        
        Returns:
            route(dict): route and its corresponding metric. i.e. {1111::/64 : 5}
    """


    try:
        output = device.parse("show ipv6 route")
    except Exception as e:
        log.error("An Exception occured: {}".format(e))
        return None

    output = output['vrf']['default']['address_family']['ipv6']['routes']

    route_metric = {}

    for key, val in output.items():
        route_metric[key] = val.get('metric')

    return route_metric

def get_ipv6_interface_ip_and_mask(device, interface):
    """ Get interface ipv6 address and mask from device

        Args:
            interface('str'): Interface to get address
            device('obj'): Device object
        
        Returns:
            None
            ipv6_address ('str'): If has multiple address will return the first one
            prefix_length ('int'): prefix length of the returned ipv6_address
    
    """

    try:
        if '.' in interface and interface.split('.')[1] == '0':
            interface = interface.split('.')[0]

        out = device.parse('show ipv6 interface {interface}'.format(interface=interface))
    except SchemaEmptyParserError as e:
        log.error('No interface information found for {}: {}'.format(interface, e))
        return None

    intf = list(out.keys())[0]

    for sub_key, sub_value in out[intf]['ipv6'].items():

        if type(sub_value) == dict:
            sub_value_keys = list(sub_value.keys())
            if 'origin' not in sub_value_keys and 'ip' in sub_value_keys:
                return sub_value['ip'], sub_value['prefix_length']
