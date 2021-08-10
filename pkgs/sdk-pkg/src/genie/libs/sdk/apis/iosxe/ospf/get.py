"""Common get info functions for OSPF"""

# Python
import os
import logging
import re

# pyATS
from pyats.easypy import runtime
from pyats.utils.objects import find, R

# Genie
from genie.utils.config import Config
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys

# LOGGING
from genie.libs.sdk.apis.iosxe.logging.get import get_logging_logs

# Utils
from genie.libs.sdk.apis.iosxe.startup_config.get import (
    get_startup_config_dict,
)
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

log = logging.getLogger(__name__)


def get_ospf_router_self_originate_metric(device, vrf, ospf_process_id):
    """ Get the OSPF advertised metric value

        Args:
            device ('obj'): Device object
            vrf (`str`): Vrf value - Default
            ospf_process_id (`int`): OSPF process ID

        Returns:
            Dictionary for metric

        Raises:
            SchemaEmptyParserError
            KeyError
    """
    metric_dict = {}

    try:
        out = device.parse("show ip ospf database router self-originate")
    except SchemaEmptyParserError as e:
        return metric_dict

    if out:
        try:
            for area in out["vrf"][vrf]["address_family"]["ipv4"]["instance"][
                ospf_process_id
            ]["areas"]:
                for lsa_type in out["vrf"][vrf]["address_family"]["ipv4"][
                    "instance"
                ][ospf_process_id]["areas"][area]["database"]["lsa_types"]:
                    for lsa in out["vrf"][vrf]["address_family"]["ipv4"][
                        "instance"
                    ][ospf_process_id]["areas"][area]["database"]["lsa_types"][
                        lsa_type
                    ][
                        "lsas"
                    ]:
                        for link in out["vrf"][vrf]["address_family"]["ipv4"][
                            "instance"
                        ][ospf_process_id]["areas"][area]["database"][
                            "lsa_types"
                        ][
                            lsa_type
                        ][
                            "lsas"
                        ][
                            lsa
                        ][
                            "ospfv2"
                        ][
                            "body"
                        ][
                            "router"
                        ][
                            "links"
                        ]:
                            if (
                                out["vrf"][vrf]["address_family"]["ipv4"][
                                    "instance"
                                ][ospf_process_id]["areas"][area]["database"][
                                    "lsa_types"
                                ][
                                    lsa_type
                                ][
                                    "lsas"
                                ][
                                    lsa
                                ][
                                    "ospfv2"
                                ][
                                    "body"
                                ][
                                    "router"
                                ][
                                    "links"
                                ][
                                    link
                                ][
                                    "type"
                                ]
                                == "stub network"
                            ):
                                continue
                            metric_dict.setdefault(link, {})
                            for topology in out["vrf"][vrf]["address_family"][
                                "ipv4"
                            ]["instance"][ospf_process_id]["areas"][area][
                                "database"
                            ][
                                "lsa_types"
                            ][
                                lsa_type
                            ][
                                "lsas"
                            ][
                                lsa
                            ][
                                "ospfv2"
                            ][
                                "body"
                            ][
                                "router"
                            ][
                                "links"
                            ][
                                link
                            ][
                                "topologies"
                            ]:
                                metric = out["vrf"][vrf]["address_family"][
                                    "ipv4"
                                ]["instance"][ospf_process_id]["areas"][area][
                                    "database"
                                ][
                                    "lsa_types"
                                ][
                                    lsa_type
                                ][
                                    "lsas"
                                ][
                                    lsa
                                ][
                                    "ospfv2"
                                ][
                                    "body"
                                ][
                                    "router"
                                ][
                                    "links"
                                ][
                                    link
                                ][
                                    "topologies"
                                ][
                                    topology
                                ][
                                    "metric"
                                ]
                                metric_dict[link].setdefault(topology, metric)
                        return metric_dict
        except KeyError as e:
            log.error(
                "Failed in retrieving OSPF advertised metric value, "
                "Error: {}".format(str(e))
            )
            return metric_dict
    return metric_dict


def get_ospf_area_of_interface(
    device,
    interface,
    process_id,
    vrf="default",
    address_family="ipv4",
    output=None,
):
    """ Get area value of an interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            vrf ('str'): VRF name
            process_id ('str'): Process id
            address_family ('str'): Address family
        Returns:
            area ('str'): If area found
            None: If area not found
        Raises:
            ValueError: Command found more than one area
    """

    log.info(
        "Getting area of interface {interface}".format(interface=interface)
    )
    if not output:
        try:
            output = device.parse(
                "show ip ospf interface {interface}".format(
                    interface=interface
                )
            )
        except SchemaEmptyParserError:
            log.info("Could not find any area")
            return None

    if process_id:
        areas = list(
            output["vrf"]
            .get(vrf, {})
            .get("address_family", {})
            .get(address_family, {})
            .get("instance", {})
            .get(process_id, {})
            .get("areas", {})
            .keys()
        )

        if len(areas) > 1:
            raise ValueError(
                "Command has returned more than one area. The following "
                "areas have been returned:\n{areas}".format(
                    areas="\n".join(areas)
                )
            )

        area = areas[0]

        log.info("Found area {area}".format(area=area))

    return area


def get_ospf_process_number(
    device, vrf="default", interface=None, output=None
):
    """ Get ospf process number

        Args:
            device ('obj'): device to run on
            vrf ('str'): vrf to search under
            interface ('str') interface to serach under
            output ('dict'): Output from parser otherwise will get from device

        Returns:
            None if error occured
            str: ospf process number

        Raises:
            SchemaEmptyParserError
    """
    if not output:
        try:
            if interface:
                output = device.parse(
                    "show ip ospf interface {interface}".format(
                        interface=interface
                    )
                )
            else:
                output = device.parse("show ip ospf")
        except SchemaEmptyParserError:
            return None

    if (
        output
        and "vrf" in output
        and vrf in output["vrf"]
        and "address_family" in output["vrf"][vrf]
        and "ipv4" in output["vrf"][vrf]["address_family"]
    ):
        for number in output["vrf"][vrf]["address_family"]["ipv4"].get(
            "instance", {}
        ):
            return number

    return None


def get_ospf_neighbors_in_state(
    device, state, neighbor_interface=None, in_state=True
):
    """ Get ospf neighbor ip_addresses that are in {state} - show
        ip ospf neighbor

        Args:
            device ('obj'): device to run on
            neighbor_interface ('str'): Neighbor interface name
            state ('str'): full/sub-string of the state you want 
                           search for
            in_state ('bool'): Check if state is in state provided

        Returns:
            list of ospf neighbor ip_addresses
                ex: ['192.168.0.1', '192.168.0.2', ...]

        Raises:
            SchemaEmptyParserError
    """

    neighbor_addresses = []

    if state:
        state = state.lower()
        if in_state:
            log.info(
                "Getting all ospf neighbors that are"
                " in state: '{}'.".format(state)
            )
        else:
            log.info(
                "Getting all ospf neighbors that are"
                " not in state: '{}'.".format(state)
            )
    else:
        log.info("Getting all ospf neighbors")

    try:
        if neighbor_interface:
            out = device.parse(
                "show ip ospf neighbor {intf}".format(intf=neighbor_interface)
            )
        else:
            out = device.parse("show ip ospf neighbor")
    except SchemaEmptyParserError:
        return neighbor_addresses

    if out and "interfaces" in out:
        for neighbor_interface in out["interfaces"]:
            for neighbor in out["interfaces"][neighbor_interface].get(
                "neighbors", {}
            ):
                if not state:
                    neighbor_addresses.append(neighbor)
                else:
                    output_state = (
                        out["interfaces"][neighbor_interface]["neighbors"][
                            neighbor
                        ].get("state", "")
                    ).lower()
                    if not output_state:
                        continue
                    if in_state:
                        if state in output_state:
                            neighbor_addresses.append(neighbor)
                    else:
                        if state not in output_state:
                            neighbor_addresses.append(neighbor)

    return neighbor_addresses


def get_ospf_neighbors_not_in_state(device, state):
    """ Get ospf neighbor ip_addresses that are in {state} - show
        ip ospf neighbor

        Args:
            device ('obj'): device to run on
            state ('str'): full/sub-string of the state you want 
                           search against

        Returns:
            list of ospf neighbor ip_addresses
                ex: ['192.168.0.1', '192.168.0.2', ...]

    """
    return get_ospf_neighbors_in_state(
        device=device, state=state, in_state=False
    )


def get_ospf_neighbors(device, neighbor_interface=None):
    """ Get ospf neighbor ip_addresses - show
        ip ospf neighbor

        Args:
            device ('obj'): device to run on
            neighbor_interface ('str'): Neighbor interface name

        Returns:
            list of ospf neighbor ip_addresses
                ex: ['192.168.0.1', '192.168.0.2', ...]

    """
    return get_ospf_neighbors_in_state(
        device=device, neighbor_interface=neighbor_interface, state=None
    )


def get_ospf_neighbors_using_interface(device, interface):
    """ Get ospf neighbor ip_addresses that are under the specified interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to search under

        Returns:
            list of ospf neighbor ip_addresses

        Raises:
            SchemaEmptyParserError
    """
    neighbor_addresses = []

    log.info("Getting all ospf neighbors under {}".format(interface))

    try:
        out = device.parse("show ip ospf neighbor")
    except SchemaEmptyParserError:
        return neighbor_addresses

    if out and "interfaces" in out and interface in out["interfaces"]:

        for neighbor in out["interfaces"][interface].get("neighbors", {}):
            neighbor_addresses.append(neighbor)

    return neighbor_addresses


def get_router_ospf_section_running_config(device, ospf_process_id):
    """ Get router OSPF section from running-config
        Args:
            device ('obj'): Device object
            ospf_process_id ('int'): OSPF router process id
        Returns:
            Dict with section
    """

    section = "router ospf {ospf_process_id}".format(
        ospf_process_id=ospf_process_id
    )
    return get_running_config_section_dict(
        device=device, section=section
    )


def get_router_ospf_section_startup_config(device, ospf_process_id):
    """ Get router OSPF section from startup-config
        Args:
            device ('obj'): Device object
            ospf_process_id ('int'): OSPF router process id
        Returns:
            Dict with section
    """

    section = "router ospf {ospf_process_id}".format(
        ospf_process_id=ospf_process_id
    )
    return get_startup_config_dict(
        device=device, section=section
    )


def get_ospf_session_count(device):
    """ Get ospf seesion count

        Args:
            device(`str`): Device str
        
        Returns:
            integer: ospf session count
        
        Raises:
            SchemaEmptyParserError
    """
    ospf_session_count = 0

    try:
        output_ospf = device.parse("show ip ospf neighbor")
    except SchemaEmptyParserError:
        return ospf_session_count

    for intf in output_ospf["interfaces"]:
        ospf_session_count += len(
            output_ospf["interfaces"].get(intf, {}).get("neighbors", {}).keys()
        )

    return ospf_session_count


def get_ospf_interfaces(device, bgp_as=None, ospf_process_id=None):
    """ Retrieve interface for ospf using OSPF Process ID

        Args:
            device ('obj'): Device object
            ospf_process_id ('int'): OSPF Process ID

        Returns:
            List of interfaces

        Raises:
            SchemaEmptyParserError
    """
    # added 'ospf_process_id' after. so keep having 'bgp_as' for backward compatibility
    if (
        (isinstance(bgp_as, int) or isinstance(ospf_process_id, int))
        and bgp_as
        and not ospf_process_id
    ):
        ospf_process_id = bgp_as

    try:
        out = device.parse("show ip ospf interface brief")
    except SchemaEmptyParserError:
        return None

    try:
        areas_dict = out["instance"][str(ospf_process_id)]["areas"]
    except KeyError:
        return None

    interfaces = []
    if areas_dict:
        for area in areas_dict.keys():
            interfaces.extend(areas_dict[area]["interfaces"].keys())
    return interfaces


def get_ospf_process_id_and_area(
    device, vrf="default", interface=None, address_family="ipv4"
):
    """ Get ospf process id and area

        Args:
            device ('obj'): device to run on
            vrf ('str'): vrf to search under
            interface ('str') interface to serach under
            address_family (`str`): Address family name

        Returns:
            None if error occured
            tuple: ospf process number and area
                ex.) (1234, ['0.0.0.4', '0.0.0.8'])
                First element that is 1234 is process number
                Second element that is ['0.0.0.4', '0.0.0.8'] is list of areas
        Raises:
            None
    """

    try:
        if interface:
            out = device.parse(
                "show ip ospf interface {interface}".format(
                    interface=interface
                )
            )
        else:
            out = device.parse("show ip ospf")
    except SchemaEmptyParserError:
        return None, None

    if (
        out
        and "vrf" in out
        and vrf in out["vrf"]
        and "address_family" in out["vrf"][vrf]
        and address_family in out["vrf"][vrf]["address_family"]
    ):
        for number, areas in out["vrf"][vrf]["address_family"][address_family][
            "instance"
        ].items():
            if "areas" in areas:
                return number, list(areas["areas"])

    return None, None

def get_ospf_global_block_range(device, process_id, output=None):
    ''' Get global block range from segment-routing
        Args:
            device ('obj'): Device object
            process_id ('str'): Ospf process id
            output ('dict'): Optional. Parsed output of command 'show ip ospf segment-routing'
        Returns:
            tuple: (
                int: Global range minimum
                int: Global range maximum
            )
        Raises:
            None
    '''

    log.info('Getting global block range from segment-routing')

    if not output:
        try:
            output = device.parse('show ip ospf segment-routing')
        except SchemaEmptyParserError:
            log.info('Could not find any block range '
                     'information for process {id}'.format(id=process_id))
            return None, None

    srgb_min=output['process_id'].get(process_id, {}).get('global_block_srgb', {}).get('range', {}).get('start', None)
    srgb_max=output['process_id'].get(process_id, {}).get('global_block_srgb', {}).get('range', {}).get('end', None)

    if (srgb_min and srgb_max):
        log.info('Found range {rmin} - {rmax}'.format(rmin=srgb_min, rmax=srgb_max))

    elif not (srgb_min or srgb_max):
        log.info('Could not find any range information')
    elif not srgb_min:
        log.info('Could not find minimum range information')
    elif not srgb_max:
        log.info('Could not find maximum range information')

    return srgb_min, srgb_max

def get_ospf_local_block_range(device, process_id, output=None):
    ''' Get local block range from segment-routing
        Args:
            device ('obj'): Device object
            process_id ('str'): Ospf process id
            output ('dict'): Optional. Parsed output of command 'show ip ospf segment-routing'
        Returns:
            tuple: (
                int: Local range minimum
                int: Local range maximum
            )
        Raises:
            None
    '''

    log.info('Getting local block range from segment-routing')

    if not output:
        try:
            output = device.parse('show ip ospf segment-routing')
        except SchemaEmptyParserError:
            log.info('Could not find any block range '
                     'information for process {id}'.format(id=process_id))
            return None, None

    srlb_min=output['process_id'].get(process_id, {}).get('local_block_srlb', {}).get('range', {}).get('start', None)
    srlb_max=output['process_id'].get(process_id, {}).get('local_block_srlb', {}).get('range', {}).get('end', None)

    if (srlb_min and srlb_max):
        log.info('Found range {rmin} - {rmax}'.format(rmin=srlb_min, rmax=srlb_max))

    elif not (srlb_min or srlb_max):
        log.info('Could not find any range information')
    elif not srlb_min:
        log.info('Could not find min range information')
    elif not srlb_max:
        log.info('Could not find max range information')

    return srlb_min, srlb_max

def get_ospf_segment_routing_lb_srlb_base_and_range(
    device, process_id, router_id
):
    """ Gets 'SRLB Base' and 'SRLB Range' values

        Args:
            device ('obj'): Device to use
            process_id ('str'): Ospf process_id
            router_id ('str'): Which router_id entry to use

        Returns:
            if can filter down to one result:
                (('int'): SRLB Base value, ('dict'): Output from parser)

        Raises:
            None
    """
    try:
        output = device.parse("show ip ospf segment-routing local-block")
    except SchemaEmptyParserError:
        return None, None

    reqs_base = R(
        [
            "instance",
            process_id,
            "areas",
            "(?P<area>.*)",
            "router_id",
            router_id,
            "srlb_base",
            "(?P<srlb_base>.*)",
        ]
    )
    found_base = find(output, reqs_base, filter_=False, all_keys=True)
    if not found_base:
        return None, None

    reqs_range = R(
        [
            "instance",
            process_id,
            "areas",
            "(?P<area>.*)",
            "router_id",
            router_id,
            "srlb_range",
            "(?P<srlb_range>.*)",
        ]
    )
    found_range = find(output, reqs_range, filter_=False, all_keys=True)
    if not found_range:
        return None, None

    return found_base[0][0], found_range[0][0]


def get_ospf_segment_routing_gb_srgb_base_and_range(
    device,
    process_id,
    router_id
):
    """ Gets 'SRGB Base' and 'SRGB Range' values

        Args:
            device ('obj'): Device to use
            process_id ('int'): Ospf process_id
            router_id ('str'): Which router_id entry to use

        Returns:
            if can filter down to one result:
                (('int'): SRGB Base value, ('dict'): Output from parser)
            if cannot filter due to lack of arguments:
                ([{key:value},{key:value}], ('dict'): Output from parser)

        Raises:
            None
    """
    try:
        output = device.parse("show ip ospf segment-routing global-block")
    except SchemaEmptyParserError:
        return None, None

    reqs_base = R(
        [
            "process_id",
            process_id,
            "routers",
            router_id,
            'srgb_base',
            "(?P<srgb_base>.*)",
        ]
    )
    found_base = find(output, reqs_base, filter_=False, all_keys=True)
    if not found_base:
        return None, None

    reqs_range = R(
        [
            "process_id",
            process_id,
            "routers",
            router_id,
            'srgb_range',
            "(?P<srgb_range>.*)",
        ]
    )
    found_range = find(output, reqs_range, filter_=False, all_keys=True)
    if not found_range:
        return None, None

    return found_base[0][0], found_range[0][0]


def get_ospf_neighbor_address_in_state(device, state=None):
    """ Gets the ospf neighbors address' in state

        Args:
            device ('obj'): Device to use
            state ('str'): full/sub-string of the state you want
                           search for

        Returns:
            ('list'): of ospf neighbor address' in state

        Raises:
            N/A
    """
    try:
        out = device.parse("show ip ospf neighbor")
    except SchemaEmptyParserError:
        return []

    addresses = []

    for intf in out.get("interfaces", {}):
        for neighbor in out["interfaces"][intf].get("neighbors", {}):
            if not state:
                addresses.append(out["interfaces"][intf]["neighbors"][neighbor].get("address"))
            elif state.lower() in out["interfaces"][intf]["neighbors"][neighbor].get("state", "").lower():
                addresses.append(out["interfaces"][intf]["neighbors"][neighbor].get("address"))

    return addresses


def get_ospf_sr_adj_sid_and_neighbor_address(device, process_id, neighbor_addresses=None):
    """ Gets adjacency sids and corresponding neighbor address.

        Args:
            device ('obj'): Device to use
            process_id ('str'): Ospf process id
            neighbor_addresses ('list'): If provided, function will only return adj-sid/neighbor_address
                                         pairs that exist in the list

        Returns:
            {(192.168.0.1, 123), (192.168.0.2, 231), ...}
    """
    try:
        out = device.parse('show ip ospf segment-routing adjacency-sid')
    except SchemaEmptyParserError:
        return {}

    ret_dict = {}

    for sid in out.get("process_id", {}).get(process_id, {}).get("adjacency_sids", {}):
        neighbor_address = out["process_id"][process_id]["adjacency_sids"][sid].get("neighbor_address")

        if neighbor_addresses:
            if neighbor_address and neighbor_address in neighbor_addresses:
                ret_dict.update({neighbor_address: sid})
        else:
            if neighbor_address:
                ret_dict.update({neighbor_address: sid})

    return ret_dict


def get_ospf_interface_affinity_bits(device, interface):
    """ Get affinity bits value of an ospf interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
        Returns:
            bits ('str'): Affinity bits
    """

    log.info("Getting Affinity bits of interface {intf}".format(intf=interface))

    cmd = 'show ip ospf interface {intf}'.format(intf=interface)
    try:
        out = device.parse(cmd)
    except Exception as e:
        log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
        return None

    reqs = R(['vrf','(.*)',
              'address_family','(.*)',
              'instance','(.*)','areas','(.*)',
              'interfaces','(.*)','teapp','(.*)',
              'affinity','bits','(?P<bits>.*)'])
    found = find([out], reqs, filter_=False, all_keys=True)
    if found:
        keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={}, 
                                    source=found, all_keys=True)
        bits = keys[0]['bits']
        log.info("Get affinity bits '{bits}' on {intf}".format(bits=bits, intf=interface))
        return bits
    else:
        log.error("Failed to get affinity bits on {intf}".format(intf=interface))
        return None


def get_ospf_process_id_on_interface(device, interface):
    """ Get ospf interface process id

        Args:
            device ('obj'): device object
            interface ('str'): interface name

        Returns:
            ospf_id ('str'): ospf process id
    """
    log.info("Getting ospf interface {intf} process id from device {dev}"
        .format(intf=interface, dev=device.name))

    cmd = 'show ip ospf interface {intf}'.format(intf=interface)
    try:
        out = device.parse(cmd)
    except Exception as e:
        log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
        return None

    reqs = R(['vrf', '(?P<vrf>.*)', 'address_family',
              '(?P<af>.*)', 'instance', '(?P<instance>.*)',
              'areas', '(?P<area>.*)', 'interfaces', interface,
              'name', '(?P<name>.*)'])

    found = find([out], reqs, filter_=False, all_keys=True)

    if found:
        keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={}, source=found, all_keys=True)
        return keys[0]['instance']
    else:
        return None