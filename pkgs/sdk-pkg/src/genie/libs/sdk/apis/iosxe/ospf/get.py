"""Common get info functions for OSPF"""

# Python
import os
import logging
import re

# pyATS
from ats.easypy import runtime
from ats.utils.objects import find, R

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


def get_ospf_process_number(device, vrf="default", interface=None):
    """ Get ospf process number

        Args:
            device ('obj'): device to run on
            vrf ('str'): vrf to search under
            interface ('str') interface to serach under
        
        Returns:
            None if error occured
            str: ospf process number

        Raises:
            SchemaEmptyParserError
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
        return None

    if (
        out
        and "vrf" in out
        and vrf in out["vrf"]
        and "address_family" in out["vrf"][vrf]
        and "ipv4" in out["vrf"][vrf]["address_family"]
    ):
        for number in out["vrf"][vrf]["address_family"]["ipv4"].get(
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


def get_ospf_interfaces(device, bgp_as):
    """ Retrieve interface for ospf using BGP AS number

        Args:
            device ('obj'): Device object
            bgp_as ('int'): BGP AS number

        Returns:
            List of interfaces

        Raises:
            SchemaEmptyParserError
    """
    try:
        out = device.parse("show ip ospf interface brief")
    except SchemaEmptyParserError:
        return None

    try:
        areas_dict = out["instance"][str(bgp_as)]["areas"]
    except KeyError:
        return None

    interfaces = []
    if areas_dict:
        for area in areas_dict.keys():
            interfaces.extend(areas_dict[area]["interfaces"].keys())
    return interfaces


def get_ospf_process_id_and_area(device, vrf='default', interface=None,
        address_family='ipv4'):
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
            if 'areas' in areas:
                return number, list(areas["areas"])

    return None, None
